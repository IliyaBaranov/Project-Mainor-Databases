from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QScrollArea, QWidget, QLabel, QHBoxLayout, QPushButton, QSizePolicy


# Function to add a row (label + value)
def add_info_row(label_text, value):
    row_layout = QHBoxLayout()
    row_layout.addWidget(QLabel(f"{label_text}"))
    row_layout.addWidget(QLabel(str(value)))
    return row_layout


class CarDetailWindow(QDialog):
    def __init__(self, car_data, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Detailed Car Information")
        self.layout = QVBoxLayout()

        # Section Separator "Main Information"
        separator1 = QLabel("---------------- Main Information ----------------")
        separator1.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(separator1)

        # Detailed Information
        self.layout.addLayout(add_info_row("Brand:", car_data[0]))
        self.layout.addLayout(add_info_row("Model:", car_data[1]))
        self.layout.addLayout(add_info_row("Country:", car_data[2]))
        self.layout.addLayout(add_info_row("Class:", car_data[3]))
        self.layout.addLayout(add_info_row("Start Year:", car_data[4]))
        self.layout.addLayout(add_info_row("End Year:", car_data[5]))
        self.layout.addLayout(add_info_row("Body Type:", car_data[6]))

        # Section Separator "Generation"
        separator2 = QLabel("---------------- Generation ----------------")
        separator2.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(separator2)

        self.layout.addLayout(add_info_row("Generation:", car_data[7]))
        self.layout.addLayout(add_info_row("Production Start Year:", car_data[8]))
        self.layout.addLayout(add_info_row("Production End Year:", car_data[9]))

        # Section Separator "Specifications"
        separator3 = QLabel("---------------- Specifications ----------------")
        separator3.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(separator3)

        self.layout.addLayout(add_info_row("Engine:", car_data[10]))
        self.layout.addLayout(add_info_row("Horsepower:", car_data[11]))
        self.layout.addLayout(add_info_row("Transmission:", car_data[12]))
        self.layout.addLayout(add_info_row("Drive Type:", car_data[13]))
        self.layout.addLayout(add_info_row("Engine Volume:", car_data[14]))
        self.layout.addLayout(add_info_row("Fuel Consumption (per 100km):", car_data[15]))
        self.layout.addLayout(add_info_row("Max Speed:", car_data[16]))

        # "Back" Button
        back_button = QPushButton("Back")
        back_button.clicked.connect(self.close)
        self.layout.addWidget(back_button)

        self.setLayout(self.layout)


# Main window with search results
class SearchResultWindow(QDialog):
    def __init__(self, results):
        super().__init__()
        self.resize(400, 300)
        self.setWindowTitle("Search Results")
        self.layout = QVBoxLayout()

        if results:
            scroll_area = QScrollArea()
            result_widget = QWidget()
            result_layout = QVBoxLayout()

            # Adding rows with results
            for row in results:
                row_layout = QHBoxLayout()

                # Main car information
                column_layout = QVBoxLayout()
                column_layout.addWidget(QLabel(f"Brand: {row[0]}"))
                column_layout.addWidget(QLabel(f"Model: {row[1]}"))
                column_layout.addWidget(QLabel(f"Start Year: {row[4]}"))

                # Button to view detailed information
                detail_button = QPushButton("Details")
                detail_button.clicked.connect(lambda checked, data=row: self.open_detail_window(data))

                # Add elements to the row
                row_layout.addLayout(column_layout)
                row_layout.addWidget(detail_button)
                result_layout.addLayout(row_layout)
                result_layout.addWidget(QLabel("\n"))

            result_widget.setLayout(result_layout)

            # Set size policy to avoid horizontal scrolling
            result_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
            scroll_area.setWidget(result_widget)
            scroll_area.setWidgetResizable(True)
            scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # Disable horizontal scroll

            self.layout.addWidget(scroll_area)
        else:
            self.layout.addWidget(QLabel("No data available."))

        self.setLayout(self.layout)


    def open_detail_window(self, car_data):
        """Opens a window with detailed car information."""
        detail_window = CarDetailWindow(car_data)
        detail_window.exec_()
