from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QScrollArea, QWidget, QLabel, QHBoxLayout, QPushButton, QSizePolicy


# Функция для добавления строки (название + значение)
def add_info_row(label_text, value):
    row_layout = QHBoxLayout()
    row_layout.addWidget(QLabel(f"{label_text}"))
    row_layout.addWidget(QLabel(str(value)))
    return row_layout


class CarDetailWindow(QDialog):
    def __init__(self, car_data, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Детальная информация о машине")
        self.layout = QVBoxLayout()

        # Разделитель "Поколение"
        separator1 = QLabel("---------------- Основные ----------------")
        separator1.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(separator1)

        # Детальная информация
        self.layout.addLayout(add_info_row("Марка:", car_data[0]))
        self.layout.addLayout(add_info_row("Модель:", car_data[1]))
        self.layout.addLayout(add_info_row("Страна:", car_data[2]))
        self.layout.addLayout(add_info_row("Класс:", car_data[3]))
        self.layout.addLayout(add_info_row("Год начала:", car_data[4]))
        self.layout.addLayout(add_info_row("Год окончания:", car_data[5]))
        self.layout.addLayout(add_info_row("Тип кузова:", car_data[6]))

        # Разделитель "Поколение"
        separator2 = QLabel("---------------- Поколение ----------------")
        separator2.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(separator2)

        self.layout.addLayout(add_info_row("Поколение:", car_data[7]))
        self.layout.addLayout(add_info_row("Год начала производства:", car_data[8]))
        self.layout.addLayout(add_info_row("Год окончания производства:", car_data[9]))

        # Разделитель "Характеристики"
        separator3 = QLabel("---------------- Характеристики ----------------")
        separator3.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(separator3)

        self.layout.addLayout(add_info_row("Двигатель:", car_data[10]))
        self.layout.addLayout(add_info_row("Л.С.:", car_data[11]))
        self.layout.addLayout(add_info_row("КПП:", car_data[12]))
        self.layout.addLayout(add_info_row("Привод:", car_data[13]))
        self.layout.addLayout(add_info_row("Объем двигателя:", car_data[14]))
        self.layout.addLayout(add_info_row("Потребление на 100км:", car_data[15]))
        self.layout.addLayout(add_info_row("Максимальная скорость:", car_data[16]))

        # Кнопка "Назад"
        back_button = QPushButton("Назад")
        back_button.clicked.connect(self.close)
        self.layout.addWidget(back_button)

        self.setLayout(self.layout)


# Основное окно с результатами поиска
class SearchResultWindow(QDialog):
    def __init__(self, results):
        super().__init__()
        self.resize(400, 300)
        self.setWindowTitle("Результаты поиска")
        self.layout = QVBoxLayout()

        if results:
            scroll_area = QScrollArea()
            result_widget = QWidget()
            result_layout = QVBoxLayout()

            # Добавляем строки с результатами
            for row in results:
                row_layout = QHBoxLayout()

                # Основная информация о машине
                column_layout = QVBoxLayout()
                column_layout.addWidget(QLabel(f"Марка: {row[0]}"))
                column_layout.addWidget(QLabel(f"Модель: {row[1]}"))
                column_layout.addWidget(QLabel(f"Год начала: {row[4]}"))

                # Кнопка для просмотра детальной информации
                detail_button = QPushButton("Подробнее")
                detail_button.clicked.connect(lambda checked, data=row: self.open_detail_window(data))

                # Добавляем элементы в строку
                row_layout.addLayout(column_layout)
                row_layout.addWidget(detail_button)
                result_layout.addLayout(row_layout)
                result_layout.addWidget(QLabel("\n"))

            result_widget.setLayout(result_layout)

            # Устанавливаем политику размеров для избежания горизонтального скролла
            result_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
            scroll_area.setWidget(result_widget)
            scroll_area.setWidgetResizable(True)
            scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # Отключаем горизонтальный скроллер

            self.layout.addWidget(scroll_area)
        else:
            self.layout.addWidget(QLabel("Нет данных для отображения."))

        self.setLayout(self.layout)


    def open_detail_window(self, car_data):
        """Открывает окно с детальной информацией о машине."""
        detail_window = CarDetailWindow(car_data)
        detail_window.exec_()
