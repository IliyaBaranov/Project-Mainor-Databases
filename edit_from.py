import sqlite3
from PyQt5.QtWidgets import (QDialog, QComboBox, QLineEdit, QPushButton, QVBoxLayout,
                             QMessageBox, QFormLayout, QCheckBox, QLabel, QHBoxLayout, QWidget)


class EditDataForm(QDialog):
    TABLE_COLUMNS = {
        "marks": {
            "name": "Название",
            "country": "Страна"},
        "models": {
            "name": "Название",
            "class": "Класс автомобиля",
            "year_from": "Год начала",
            "year_to": "Год окончания",
            "body_type": "Тип кузова"
        },
        "generations": {
            "name": "Название",
            "year_start": "Год начала",
            "year_stop": "Год окончания"},
        "specifications": {
            "engine_type": "Тип двигателя",
            "horse_power": "Мощность (л.с.)",
            "transmission": "Трансмиссия",
            "drive": "Привод",
            "volume": "Объем двигателя",
            "consumption_mixed": "Расход (смешанный)",
            "max_speed": "Макс. скорость",
            "price": "Цена"
        }
    }

    TABLE_NAMES = {
        "marks": "Марки",
        "models": "Модели",
        "generations": "Поколения",
        "specifications": "Характеристики"
    }

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Редактирование данных")
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()

        # Поля для ввода данных
        input_fields = [
            ("Марка:", "input_mark"),
            ("Модель:", "input_model"),
            ("Поколение:", "input_generation"),
            ("Характеристика:", "input_specification")
        ]

        for label_text, attr_name in input_fields:
            row_layout = QHBoxLayout()
            label = QLabel(label_text)
            combo_box = QComboBox()
            combo_box.setEnabled(attr_name == "input_mark")  # Только для марки включено по умолчанию
            row_layout.addWidget(label)
            row_layout.addWidget(combo_box)
            self.layout.addLayout(row_layout)
            setattr(self, attr_name, combo_box)

        # Чекбоксы и поля ввода для таблиц
        self.checkboxes = {}
        self.forms = {}

        for table, columns in self.TABLE_COLUMNS.items():
            localized_table_name = self.TABLE_NAMES[table]
            checkbox = QCheckBox(localized_table_name)
            checkbox.setEnabled(False)
            checkbox.stateChanged.connect(self.toggle_form)
            self.checkboxes[table] = checkbox
            self.layout.addWidget(checkbox)

            form_widget = QWidget()
            form_layout = QFormLayout(form_widget)

            for column, label in columns.items():
                row_layout = QHBoxLayout()
                label_widget = QLabel(f"{label}:")
                line_edit = QLineEdit()
                line_edit.setPlaceholderText(f"Введите {label}")
                line_edit.setEnabled(False)
                row_layout.addWidget(label_widget)
                row_layout.addWidget(line_edit)
                form_layout.addRow(row_layout)
                self.forms[f"{table}.{column}"] = line_edit

            form_widget.setVisible(False)
            self.layout.addWidget(form_widget)
            self.forms[table] = form_widget

        # Кнопки
        self.btn_update = QPushButton("Обновить")
        self.btn_update.setEnabled(False)
        self.btn_update.clicked.connect(self.update_records)

        self.btn_cancel = QPushButton("Отмена")
        self.btn_cancel.clicked.connect(self.close)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.btn_update)
        button_layout.addWidget(self.btn_cancel)
        self.layout.addLayout(button_layout)

        self.setLayout(self.layout)

        # Привязка сигналов
        self.input_mark.currentTextChanged.connect(self.populate_models)
        self.input_model.currentTextChanged.connect(self.populate_generations)
        self.input_generation.currentTextChanged.connect(self.populate_specifications)
        self.input_generation.currentTextChanged.connect(self.enable_checkboxes)

        self.populate_marks()

    def populate_marks(self):
        try:
            conn = sqlite3.connect('cars.db')
            cursor = conn.cursor()
            cursor.execute("SELECT id, name FROM marks")
            records = cursor.fetchall()
            for record_id, record_name in records:
                self.input_mark.addItem(record_name, record_id)
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка базы данных: {e}")
        finally:
            conn.close()

    def populate_models(self):
        self.input_model.clear()
        self.input_generation.clear()
        self.input_specification.clear()
        self.input_model.setEnabled(False)
        self.input_generation.setEnabled(False)
        self.input_specification.setEnabled(False)

        if self.input_mark.currentData():
            mark_id = self.input_mark.currentData()
            try:
                conn = sqlite3.connect('cars.db')
                cursor = conn.cursor()
                cursor.execute("SELECT id, name FROM models WHERE mark_id = ?", (mark_id,))
                records = cursor.fetchall()
                for record_id, record_name in records:
                    self.input_model.addItem(record_name, record_id)
                self.input_model.setEnabled(bool(records))
            except sqlite3.Error as e:
                QMessageBox.critical(self, "Ошибка", f"Ошибка базы данных: {e}")
            finally:
                conn.close()

    def populate_generations(self):
        """
        Заполняет список поколений на основе выбранной модели.
        """
        self.input_generation.clear()
        self.input_specification.clear()
        self.input_generation.setEnabled(False)
        self.input_specification.setEnabled(False)

        model_id = self.input_model.currentData()  # Получаем выбранный model_id
        if model_id:
            try:
                conn = sqlite3.connect('cars.db')
                cursor = conn.cursor()
                # Фильтрация поколений по model_id
                cursor.execute("SELECT id, name FROM generations WHERE model_id = ?", (model_id,))
                records = cursor.fetchall()

                for record_id, record_name in records:
                    self.input_generation.addItem(record_name, record_id)  # Добавляем поколение в выпадающий список
                if records:
                    self.input_generation.setEnabled(True)

            except sqlite3.Error as e:
                QMessageBox.critical(self, "Ошибка", f"Ошибка базы данных: {e}")
            finally:
                conn.close()

    def populate_specifications(self):
        """ Заполняет список характеристик на основе выбранного model_id. """
        self.input_specification.clear()
        self.input_specification.setEnabled(False)

        model_id = self.input_model.currentData()  # Получаем model_id
        if model_id:
            try:
                conn = sqlite3.connect('cars.db')
                cursor = conn.cursor()
                # Фильтрация характеристик по model_id
                cursor.execute("SELECT id, engine_type FROM specifications WHERE model_id = ?", (model_id,))
                records = cursor.fetchall()

                for record_id, record_name in records:
                    self.input_specification.addItem(record_name, record_id)  # Добавляем характеристики в список
                if records:
                    self.input_specification.setEnabled(True)

            except sqlite3.Error as e:
                QMessageBox.critical(self, "Ошибка", f"Ошибка базы данных: {e}")
            finally:
                conn.close()

    def enable_checkboxes(self):
        """
        Активирует чекбоксы и кнопки после выбора спецификации.
        """
        if self.input_specification.currentData():  # Проверка, выбрана ли характеристика
            for checkbox in self.checkboxes.values():
                checkbox.setEnabled(True)
            self.btn_update.setEnabled(True)
        else:
            for checkbox in self.checkboxes.values():
                checkbox.setEnabled(False)
            self.btn_update.setEnabled(False)

    def toggle_form(self):
        for table, checkbox in self.checkboxes.items():
            form_widget = self.forms[table]
            form_widget.setVisible(checkbox.isChecked())
            for column in self.TABLE_COLUMNS[table].keys():
                field = self.forms.get(f"{table}.{column}")
                if field:
                    field.setEnabled(checkbox.isChecked())
        self.adjustSize()

    def update_records(self):
        specification_id = self.input_specification.currentData()

        try:
            conn = sqlite3.connect('cars.db')
            cursor = conn.cursor()

            # Создаем словарь для сопоставления таблиц с соответствующими идентификаторами
            table_id_map = {
                "marks": self.input_mark.currentData,
                "models": self.input_model.currentData,
                "generations": self.input_generation.currentData,
                "specifications": lambda: specification_id  # Лямбда для постоянного значения
            }

            for table, checkbox in self.checkboxes.items():
                if checkbox.isChecked():
                    for column, label in self.TABLE_COLUMNS[table].items():
                        key = f"{table}.{column}"
                        new_value = self.forms[key].text()
                        if new_value:
                            identifier = table_id_map[table]()  # Получаем идентификатор динамически
                            cursor.execute(
                                f"UPDATE {table} SET {column} = ? WHERE id = ?",
                                (new_value, identifier)
                            )

            conn.commit()

            QMessageBox.information(self, "Успех", "Данные успешно изменены.")

        except sqlite3.Error as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка базы данных: {e}")
        finally:
            conn.close()
