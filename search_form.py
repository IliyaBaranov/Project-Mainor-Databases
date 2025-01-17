import sqlite3
from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QWidget, QComboBox, QFormLayout, \
    QGroupBox, QHBoxLayout

from delete_car_form import DeleteCarForm
from edit_from import EditDataForm
from new_car_form import NewCarForm
from searh_result_form import SearchResultWindow


class SearchForm(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Car Search")
        self.layout = QVBoxLayout()

        # Dictionary for field configuration
        fields = [
            ("Car Brand:", "input_brand", QComboBox, self.update_all_fields),
            ("Country:", "input_country", QComboBox, None),
            ("Model:", "input_model", QComboBox, self.update_classes_and_bodies),
            ("Car Class:", "input_class", QComboBox, None),
            ("Body Type:", "input_body", QComboBox, None),
        ]

        for label_text, attr_name, widget_class, signal_handler in fields:
            row_layout = QHBoxLayout()
            label = QLabel(label_text)
            widget = widget_class()
            setattr(self, attr_name, widget)
            row_layout.addWidget(label)
            row_layout.addWidget(widget)
            self.layout.addLayout(row_layout)
            if signal_handler:
                widget.currentIndexChanged.connect(signal_handler)

        # Fields for production years
        self.layout.addWidget(QLabel("Production Year (from - to):"))
        self.input_year_from = QLineEdit()
        self.input_year_to = QLineEdit()
        self.layout.addWidget(self.input_year_from)
        self.layout.addWidget(self.input_year_to)

        # Buttons
        buttons = [
            ("Search", self.perform_search),
            ("New Car", self.open_new_car_form),
            ("Edit Data", self.update_record),
            ("Delete Car", self.delete_car_by_id),
            ("Exit", self.close),
        ]

        for btn_text, btn_handler in buttons:
            button = QPushButton(btn_text)
            button.clicked.connect(btn_handler)
            self.layout.addWidget(button)

        # Group for search results
        self.result_group = QGroupBox("Search Results")
        self.result_layout = QFormLayout()
        self.result_group.setLayout(self.result_layout)
        self.layout.addWidget(self.result_group)
        self.result_group.hide()

        # Set main layout
        self.setLayout(self.layout)

        # Populate "Car Brand" field and update other fields
        self.populate_combobox(self.input_brand, "SELECT DISTINCT name FROM marks")
        self.update_all_fields()

    def populate_combobox(self, combobox, query, params=()):
        combobox.clear()
        combobox.addItem("")  # Add empty value
        try:
            conn = sqlite3.connect('cars.db', check_same_thread=False)
            cursor = conn.cursor()
            cursor.execute(query, params)
            results = cursor.fetchall()
            if results:
                for row in results:
                    combobox.addItem(row[0])
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Error", f"Database Error: {e}")
        finally:
            conn.close()

    def update_all_fields(self):
        brand = self.input_brand.currentText()

        # Update countries
        if brand:
            query = "SELECT DISTINCT country FROM marks WHERE name = ?"
            self.populate_combobox(self.input_country, query, (brand,))
        else:
            self.populate_combobox(self.input_country, "SELECT DISTINCT country FROM marks")

        # Update models
        if brand:
            query = """
                SELECT DISTINCT models.name
                FROM models
                JOIN marks ON models.mark_id = marks.id
                WHERE marks.name = ?
            """
            self.populate_combobox(self.input_model, query, (brand,))
        else:
            self.populate_combobox(self.input_model, "SELECT DISTINCT name FROM models")

        self.update_classes_and_bodies()

    def update_classes_and_bodies(self):
        model = self.input_model.currentText()

        # Update class
        if model:
            query = """
                SELECT DISTINCT class
                FROM models
                WHERE name = ?
            """
            self.populate_combobox(self.input_class, query, (model,))
        else:
            self.populate_combobox(self.input_class, "SELECT DISTINCT class FROM models")

        # Update body type
        if model:
            query = """
                SELECT DISTINCT body_type
                FROM models
                WHERE name = ?
            """
            self.populate_combobox(self.input_body, query, (model,))
        else:
            self.populate_combobox(self.input_body, "SELECT DISTINCT body_type FROM models")

    def perform_search(self):
        brand = self.input_brand.currentText()
        model = self.input_model.currentText()
        country = self.input_country.currentText()
        car_class = self.input_class.currentText()
        body_type = self.input_body.currentText()
        year_from = self.input_year_from.text()
        year_to = self.input_year_to.text()

        try:
            conn = sqlite3.connect('cars.db')
            cursor = conn.cursor()

            # Dynamic SQL Query
            query = """
                SELECT 
                    Marks.name AS MarkName, 
                    Marks.country AS Country, 
                    Models.name AS ModelName, 
                    Models.class AS CarClass, 
                    Models.year_from AS YearFrom, 
                    Models.year_to AS YearTo, 
                    Models.body_type AS BodyType, 
                    Generations.name AS GenerationName, 
                    Generations.year_start AS GenerationStart, 
                    Generations.year_stop AS GenerationEnd, 
                    Specifications.engine_type AS EngineType, 
                    Specifications.horse_power AS HorsePower, 
                    Specifications.transmission AS Transmission, 
                    Specifications.drive AS DriveType, 
                    Specifications.volume AS EngineVolume, 
                    Specifications.consumption_mixed AS ConsumptionMixed, 
                    Specifications.max_speed AS MaxSpeed
                FROM 
                    Marks
                INNER JOIN 
                    Models ON Marks.id = Models.mark_id
                INNER JOIN 
                    Generations ON Models.id = Generations.model_id
                INNER JOIN 
                    Specifications ON Models.id = Specifications.model_id
                WHERE 1=1
            """

            params = []
            filters = {
                "Marks.name =": brand,
                "Models.name =": model,
                "Marks.country =": country,
                "Models.class =": car_class,
                "Models.body_type =": body_type,
                "Generations.year_start >= ": year_from,
                "Generations.year_stop <= ": year_to
            }

            for field, value in filters.items():
                if value:
                    query += f" AND {field} ?"
                    params.append(value)

            cursor.execute(query, tuple(params))
            results = cursor.fetchall()

            if results:
                self.search_result_window = SearchResultWindow(results)
                self.search_result_window.exec_()
            else:
                QMessageBox.information(self, "Search Results", "No data to display.")

        except sqlite3.Error as e:
            QMessageBox.critical(self, "Error", f"Database Error: {e}")
        finally:
            if conn:
                conn.close()

    def open_new_car_form(self):
        self.new_car_form = NewCarForm()
        self.new_car_form.exec_()

    def update_record(self):
        self.edit_data_form = EditDataForm()
        self.edit_data_form.exec_()

    def delete_car_by_id(self):
        self.delete_car_form = DeleteCarForm()
        self.delete_car_form.exec_()
