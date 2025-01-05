from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
import sqlite3


class DeleteCarForm(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Delete from Specifications")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Field for entering ID of Specifications
        self.label_id = QLabel("Enter the ID of Specifications to delete:")
        self.input_delete_id = QLineEdit()
        self.input_delete_id.setPlaceholderText("Specifications ID")

        # Buttons
        self.btn_delete = QPushButton("Delete")
        self.btn_delete.clicked.connect(self.delete_specification)

        self.btn_cancel = QPushButton("Cancel")
        self.btn_cancel.clicked.connect(self.close)

        # Adding elements to the layout
        layout.addWidget(self.label_id)
        layout.addWidget(self.input_delete_id)
        layout.addWidget(self.btn_delete)
        layout.addWidget(self.btn_cancel)

        self.setLayout(layout)

    def delete_specification(self):
        specification_id = self.input_delete_id.text().strip()

        # Check if the ID is numeric
        if not specification_id.isdigit():
            QMessageBox.warning(self, "Error", "Please enter a valid Specifications ID.")
            return

        try:
            # Connect to the database
            conn = sqlite3.connect('cars.db')
            cursor = conn.cursor()

            # Check if a record with the specified ID exists in the Specifications table
            cursor.execute("SELECT id FROM Specifications WHERE id = ?", (specification_id,))
            if not cursor.fetchone():
                QMessageBox.warning(self, "Error", f"No record found with ID {specification_id} in Specifications.")
                return

            # Delete the record from the Specifications table
            cursor.execute("DELETE FROM Specifications WHERE id = ?", (specification_id,))

            # Commit the transaction
            conn.commit()

            # Notify the user of the successful deletion
            QMessageBox.information(self, "Success", f"Record with ID {specification_id} was successfully deleted from Specifications.")

        except sqlite3.Error as e:
            # Rollback the transaction in case of an error
            conn.rollback()
            QMessageBox.critical(self, "Error", f"Database error: {e}")

        finally:
            # Close the database connection
            conn.close()
