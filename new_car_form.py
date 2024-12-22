import sqlite3
from PyQt5.QtWidgets import (QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox,
                             QDialog, QComboBox, QCheckBox, QHBoxLayout, QWidget)


def fetch_data(query, combo_box=None):
    """
    Выполняет SQL-запрос и возвращает данные.
    Если передан combo_box, добавляет данные в выпадающий список.

    :param query: SQL-запрос для выполнения.
    :param combo_box: Виджет QComboBox (опционально).
    :return: Список значений из результата запроса.
    """
    try:
        with sqlite3.connect('cars.db') as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            results = [row[0] for row in cursor.fetchall()]

            if combo_box:  # Если передан combo_box, заполняем его данными
                combo_box.addItems(results)

            return results
    except sqlite3.Error as e:
        print(f"Ошибка выполнения запроса: {e}")
        return []


class NewCarForm(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Новый автомобиль")
        self.setup_ui()

    def setup_ui(self):
        self.layout = QVBoxLayout()

        self.input_widget = self.create_input_widget()
        # Чекбоксы
        self.checkbox_styling = self.create_checkbox("Стайлинг", self.toggle_styling_params)
        self.styling_widget = self.create_styling_widget()

        self.checkbox_additional = self.create_checkbox("Дополнительные параметры", self.toggle_additional_params)
        self.additional_widget = self.create_additional_widget()

        # Кнопки управления
        self.create_button("Сохранить", self.save_new_car)
        self.create_button("Выход", self.close)

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
        # Создаем основной виджет
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)
        self.layout.addWidget(widget)

        self.input_fields = {}
        self.add_field(layout, "Марка:", "input_mark", "line_edit")
        self.add_field(layout, "Модель:", "input_model", "line_edit")
        self.add_field(layout, "Страна производства:", "combo_country", "combo_box", lambda cb: cb.addItems(fetch_data("SELECT DISTINCT country FROM Marks")))
        self.add_field(layout, "Класс автомобиля:", "combo_class", "combo_box", lambda cb: cb.addItems(fetch_data("SELECT DISTINCT class FROM Models WHERE class IS NOT NULL")))
        self.add_field(layout, "Тип кузова:", "combo_body_type", "combo_box", lambda cb: cb.addItems(fetch_data("SELECT DISTINCT body_type FROM Models WHERE body_type IS NOT NULL")))
        self.add_field(layout, "Год начала производства:", "input_year_from", "line_edit")
        self.add_field(layout, "Год окончания производства:", "input_year_to", "line_edit")
        self.add_field(layout, "Цена:", "input_price", "line_edit")

        return widget

    def create_styling_widget(self):
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)
        widget.hide()
        self.layout.addWidget(widget)

        self.styling_fields = {}
        self.add_field(layout, "Поколение:", "generation", "line_edit")
        self.add_field(layout, "Год начала поколения:", "generation_year_from", "line_edit")
        self.add_field(layout, "Год окончания поколения:", "generation_year_to", "line_edit")

        return widget

    def create_additional_widget(self):
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)
        widget.hide()
        self.layout.addWidget(widget)

        self.additional_fields = {}
        self.add_field(layout, "Двигатель:", "engine_type", "combo_box", lambda cb: cb.addItems(fetch_data("SELECT DISTINCT engine_type FROM Specifications WHERE engine_type IS NOT NULL")))
        self.add_field(layout, "КПП (трансмиссия):", "transmission", "combo_box", lambda cb: cb.addItems(fetch_data("SELECT DISTINCT transmission FROM Specifications WHERE transmission IS NOT NULL")))
        self.add_field(layout, "Привод:", "drive", "combo_box", lambda cb: cb.addItems(fetch_data("SELECT DISTINCT drive FROM Specifications WHERE drive IS NOT NULL")))
        self.add_field(layout, "Л.С.:", "horse_power", "line_edit")
        self.add_field(layout, "Объём двигателя:", "volume", "line_edit")
        self.add_field(layout, "Потребление на 100 км:", "consumption_mixed", "line_edit")
        self.add_field(layout, "Макс. скорость:", "max_speed", "line_edit")

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

        # Главные поля
        main = {key: (field.text()) for key, field in self.input_fields.items()}
        # Поля стайлинга
        styling = {key: (field.text() if field else "Не указано") for key, field in self.styling_fields.items()}
        # Дополнительные характеристики
        specs = {key: (field.currentText() if isinstance(field, QComboBox) else field.text()) or "Не указано" for key, field in self.additional_fields.items()}

        try:
            with sqlite3.connect('cars.db') as conn:
                cursor = conn.cursor()

                # Вставка или получение ID марки
                cursor.execute("""
                    INSERT OR IGNORE INTO Marks (name, country)
                    VALUES (?, ?)
                """, (main["mark_name"], main["country"]))
                cursor.execute("SELECT id FROM Marks WHERE name = ?", (main["mark_name"],))
                mark_id = cursor.fetchone()[0]

                # Вставка модели
                cursor.execute("""
                    INSERT INTO Models (name, year_from, year_to, class, body_type, mark_id)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (main["model_name"], main["year_from"], main["year_to"], main["car_class"], main["body_type"],
                      mark_id))
                model_id = cursor.lastrowid

                # Вставка поколения
                cursor.execute("""
                    INSERT INTO Generations (name, year_start, year_stop, model_id)
                    VALUES (?, ?, ?, ?)
                """, (styling.get("generation"), styling.get("generation_year_from"), styling.get("generation_year_to"),
                      model_id))

                # Вставка спецификаций
                cursor.execute("""
                    INSERT INTO Specifications (engine_type, transmission, volume, consumption_mixed, max_speed, drive, horse_power, model_id, price)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    specs.get("engine_type"), specs.get("transmission"), specs.get("volume"),
                    specs.get("consumption_mixed"), specs.get("max_speed"), specs.get("drive"),
                    specs.get("horse_power"), model_id, main["price"]
                ))

                conn.commit()
                QMessageBox.information(self, "Успех", "Автомобиль успешно добавлен.")
                self.close()

        except sqlite3.Error as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка базы данных: {e}")

    def validate_fields(self):
        """
        Проверяет обязательные поля на наличие данных.
        """
        required_fields = {
            "Марка": self.input_mark.text(),
            "Модель": self.input_model.text()
        }

        for field_name, value in required_fields.items():
            if not value.strip():
                QMessageBox.critical(self, "Ошибка", f"Поле \"{field_name}\" не должно быть пустым.")
                return False

        return True
