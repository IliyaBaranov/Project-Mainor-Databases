import sqlite3
from PyQt5.QtWidgets import (QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox,
                             QDialog, QComboBox, QCheckBox, QHBoxLayout, QWidget)


def fetch_data(query, combo_box=None):
    """
    Executes an SQL query and returns the data.
    If a combo_box is provided, populates it with the data.

    :param query: SQL query to execute.
    :param combo_box: QComboBox widget (optional).
    :return: List of values from the query result.
    """
    try:
        with sqlite3.connect('cars.db') as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            results = [row[0] for row in cursor.fetchall()]

            if combo_box:  # If combo_box is provided, populate it with data
                combo_box.addItems(results)

            return results
    except sqlite3.Error as e:
        print(f"Error executing query: {e}")
        return []


class NewCarForm(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("New Car")
        self.setup_ui()

    def setup_ui(self):
        self.layout = QVBoxLayout()

        self.input_widget = self.create_input_widget()
        # Checkboxes
        self.checkbox_styling = self.create_checkbox("Styling", self.toggle_styling_params)
        self.styling_widget = self.create_styling_widget()

        self.checkbox_additional = self.create_checkbox("Additional Parameters", self.toggle_additional_params)
        self.additional_widget = self.create_additional_widget()

        # Control buttons
        self.create_button("Save", self.save_new_car)
        self.create_button("Exit", self.close)

        self.setLayout(self.layout)

    def add_field(self, layout, label_text, attr_name, field_type="line_edit", load_func=None):
        h_layout = QHBoxLayout()
        label = QLabel(label_text)

        if field_type == "line_edit":
            field = QLineEdit()
        elif field_type == "combo_box":
            field = QComboBox()
            if load_func:
                load_func(field)
        else:
            raise ValueError("Invalid field_type. Use 'line_edit' or 'combo_box'.")

        setattr(self, attr_name, field)
        h_layout.addWidget(label)
        h_layout.addWidget(field)
        layout.addLayout(h_layout)

    def create_checkbox(self, label_text, toggle_func):
        checkbox = QCheckBox(label_text)
        checkbox.stateChanged.connect(toggle_func)
        self.layout.addWidget(checkbox)
        return checkbox

    def create_button(self, label_text, click_func):
        button = QPushButton(label_text)
        button.clicked.connect(click_func)
        self.layout.addWidget(button)

    def create_input_widget(self):
        # Create the main widget
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)
        self.layout.addWidget(widget)

        self.input_fields = {}
        self.add_field(layout, "Brand:", "input_mark", "line_edit")
        self.add_field(layout, "Model:", "input_model", "line_edit")
        self.add_field(layout, "Country of Manufacture:", "combo_country", "combo_box", lambda cb: cb.addItems(fetch_data("SELECT DISTINCT country FROM Marks")))
        self.add_field(layout, "Car Class:", "combo_class", "combo_box", lambda cb: cb.addItems(fetch_data("SELECT DISTINCT class FROM Models WHERE class IS NOT NULL")))
        self.add_field(layout, "Body Type:", "combo_body_type", "combo_box", lambda cb: cb.addItems(fetch_data("SELECT DISTINCT body_type FROM Models WHERE body_type IS NOT NULL")))
        self.add_field(layout, "Start Year of Production:", "input_year_from", "line_edit")
        self.add_field(layout, "End Year of Production:", "input_year_to", "line_edit")
        self.add_field(layout, "Price:", "input_price", "line_edit")

        return widget

    def create_styling_widget(self):
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)
        widget.hide()
        self.layout.addWidget(widget)

        self.styling_fields = {}
        self.add_field(layout, "Generation:", "generation", "line_edit")
        self.add_field(layout, "Generation Start Year:", "generation_year_from", "line_edit")
        self.add_field(layout, "Generation End Year:", "generation_year_to", "line_edit")

        return widget

    def create_additional_widget(self):
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)
        widget.hide()
        self.layout.addWidget(widget)

        self.additional_fields = {}
        self.add_field(layout, "Engine:", "engine_type", "combo_box", lambda cb: cb.addItems(fetch_data("SELECT DISTINCT engine_type FROM Specifications WHERE engine_type IS NOT NULL")))
        self.add_field(layout, "Transmission:", "transmission", "combo_box", lambda cb: cb.addItems(fetch_data("SELECT DISTINCT transmission FROM Specifications WHERE transmission IS NOT NULL")))
        self.add_field(layout, "Drive:", "drive", "combo_box", lambda cb: cb.addItems(fetch_data("SELECT DISTINCT drive FROM Specifications WHERE drive IS NOT NULL")))
        self.add_field(layout, "Horsepower:", "horse_power", "line_edit")
        self.add_field(layout, "Engine Volume:", "volume", "line_edit")
        self.add_field(layout, "Fuel Consumption (per 100 km):", "consumption_mixed", "line_edit")
        self.add_field(layout, "Max Speed:", "max_speed", "line_edit")

        return widget

    def toggle_styling_params(self):
        self.styling_widget.setVisible(self.checkbox_styling.isChecked())
        self.adjustSize()

    def toggle_additional_params(self):
        self.additional_widget.setVisible(self.checkbox_additional.isChecked())
        self.adjustSize()

    def save_new_car(self):
        if not self.validate_fields():
            return

        # Main fields
        main = {
            "mark_name": self.input_mark.text(),
            "model_name": self.input_model.text(),
            "country": self.combo_country.currentText(),
            "car_class": self.combo_class.currentText(),
            "body_type": self.combo_body_type.currentText(),
            "year_from": self.input_year_from.text(),
            "year_to": self.input_year_to.text(),
            "price": self.input_price.text(),
        }
        # Styling fields
        styling = {
            "generation": self.generation.text(),
            "generation_year_from": self.generation_year_from.text(),
            "generation_year_to": self.generation_year_to.text(),
        }
        # Additional specifications
        specs = {
            "engine_type": self.engine_type.currentText(),
            "transmission": self.transmission.currentText(),
            "drive": self.drive.currentText(),
            "horse_power": self.horse_power.text(),
            "volume": self.volume.text(),
            "consumption_mixed": self.consumption_mixed.text(),
            "max_speed": self.max_speed.text(),
        }

        try:
            with sqlite3.connect('cars.db') as conn:
                cursor = conn.cursor()

                # Insert or get brand ID
                cursor.execute("""
                    INSERT OR IGNORE INTO Marks (name, country)
                    VALUES (?, ?)
                """, (main["mark_name"], main["country"]))
                cursor.execute("SELECT id FROM Marks WHERE name = ?", (main["mark_name"],))
                mark_id = cursor.fetchone()[0]

                # Insert model
                cursor.execute("""
                    INSERT INTO Models (name, year_from, year_to, class, body_type, mark_id)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (main["model_name"], main["year_from"], main["year_to"], main["car_class"], main["body_type"],
                      mark_id))
                model_id = cursor.lastrowid

                # Insert generation
                cursor.execute("""
                    INSERT INTO Generations (name, year_start, year_stop, model_id)
                    VALUES (?, ?, ?, ?)
                """, (styling.get("generation"), styling.get("generation_year_from"), styling.get("generation_year_to"),
                      model_id))

                # Insert specifications
                cursor.execute("""
                    INSERT INTO Specifications (engine_type, transmission, volume, consumption_mixed, max_speed, drive, horse_power, model_id, price)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    specs.get("engine_type"), specs.get("transmission"), specs.get("volume"),
                    specs.get("consumption_mixed"), specs.get("max_speed"), specs.get("drive"),
                    specs.get("horse_power"), model_id, main["price"]
                ))

                conn.commit()
                QMessageBox.information(self, "Success", "Car successfully added.")
                self.close()

        except sqlite3.Error as e:
            QMessageBox.critical(self, "Error", f"Database error: {e}")

    def validate_fields(self):
        """
        Checks if the required fields have data.
        """
        required_fields = {
            "Brand": self.input_mark.text(),
            "Model": self.input_model.text()
        }

        for field_name, value in required_fields.items():
            if not value.strip():
                QMessageBox.critical(self, "Error", f"The field \"{field_name}\" cannot be empty.")
                return False

        return True
