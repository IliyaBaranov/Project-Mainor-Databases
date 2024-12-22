from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
import sqlite3


class DeleteCarForm(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Удаление из Specifications")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Поле для ввода ID Specifications
        self.label_id = QLabel("Введите ID Specifications для удаления:")
        self.input_delete_id = QLineEdit()
        self.input_delete_id.setPlaceholderText("ID Specifications")

        # Кнопки
        self.btn_delete = QPushButton("Удалить")
        self.btn_delete.clicked.connect(self.delete_specification)

        self.btn_cancel = QPushButton("Отмена")
        self.btn_cancel.clicked.connect(self.close)

        # Добавляем элементы в макет
        layout.addWidget(self.label_id)
        layout.addWidget(self.input_delete_id)
        layout.addWidget(self.btn_delete)
        layout.addWidget(self.btn_cancel)

        self.setLayout(layout)

    def delete_specification(self):
        specification_id = self.input_delete_id.text().strip()

        # Проверяем, что ID — числовое
        if not specification_id.isdigit():
            QMessageBox.warning(self, "Ошибка", "Введите корректный ID Specifications.")
            return

        try:
            # Подключаемся к базе данных
            conn = sqlite3.connect('cars.db')
            cursor = conn.cursor()

            # Проверяем, существует ли запись с таким ID в таблице Specifications
            cursor.execute("SELECT id FROM Specifications WHERE id = ?", (specification_id,))
            if not cursor.fetchone():
                QMessageBox.warning(self, "Ошибка", f"Запись с ID {specification_id} не найдена в Specifications.")
                return

            # Удаляем запись из таблицы Specifications
            cursor.execute("DELETE FROM Specifications WHERE id = ?", (specification_id,))

            # Подтверждаем транзакцию
            conn.commit()

            # Уведомляем пользователя об успешном удалении
            QMessageBox.information(self, "Успех", f"Запись с ID {specification_id} успешно удалена из Specifications.")

        except sqlite3.Error as e:
            # Откатываем транзакцию в случае ошибки
            conn.rollback()
            QMessageBox.critical(self, "Ошибка", f"Ошибка базы данных: {e}")

        finally:
            # Закрываем соединение с базой данных
            conn.close()
