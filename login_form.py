import sys
import hashlib
import sqlite3
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QMenuBar,
                             QMenu, QAction)
from search_form import SearchForm


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def initialize_db():
    try:
        conn = sqlite3.connect('cars.db')
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                login TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            );
        """)
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database error during initialization: {e}")
    finally:
        if conn:
            conn.close()


def authenticate_user(login, password):
    try:
        conn = sqlite3.connect('cars.db')
        cursor = conn.cursor()

        query = "SELECT password FROM Employees WHERE login = ?"
        cursor.execute(query, (login,))
        result = cursor.fetchone()

        if result:
            stored_hashed_password = result[0]
            return stored_hashed_password == hash_password(password)
        return False
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False
    finally:
        if conn:
            conn.close()


def add_user(name, login, password, add_user_form=None):
    try:
        conn = sqlite3.connect('cars.db')
        cursor = conn.cursor()

        query_check = "SELECT 1 FROM Employees WHERE login = ? LIMIT 1"
        cursor.execute(query_check, (login,))
        if cursor.fetchone():
            QMessageBox.warning(None, "Error", "A user with this login already exists!")
            return

        hashed_password = hash_password(password)
        query_insert = "INSERT INTO Employees (name, password, login) VALUES (?, ?, ?);"
        cursor.execute(query_insert, (name, hashed_password, login))
        conn.commit()
        QMessageBox.information(None, "Success", "User successfully added!")

        if add_user_form:
            add_user_form.close()

    except sqlite3.Error as e:
        QMessageBox.warning(None, "Error", f"Database error: {e}")
        sys.exit()

    finally:
        if conn:
            conn.close()


class BaseForm(QWidget):
    def add_label_and_input(self, label_text, is_password=False):
        label = QLabel(label_text)
        input_field = QLineEdit()
        if is_password:
            input_field.setEchoMode(QLineEdit.Password)
        self.layout.addWidget(label)
        self.layout.addWidget(input_field)
        return input_field

    def add_button(self, text, callback):
        button = QPushButton(text)
        button.clicked.connect(callback)
        self.layout.addWidget(button)
        return button


class LoginForm(BaseForm):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Login")

        self.layout = QVBoxLayout()

        self.menubar = QMenuBar(self)
        self.menu = QMenu("File", self)
        self.new_user_action = QAction("New User", self)
        self.new_user_action.triggered.connect(self.open_add_user_form)
        self.menu.addAction(self.new_user_action)
        self.menubar.addMenu(self.menu)
        self.layout.setMenuBar(self.menubar)

        self.input_login = self.add_label_and_input("Login:")
        self.input_password = self.add_label_and_input("Password:", is_password=True)

        self.add_button("Sign In", self.handle_login)
        self.add_button("Exit", self.close)

        self.setLayout(self.layout)

    def handle_login(self):
        login = self.input_login.text()
        password = self.input_password.text()

        if authenticate_user(login, password):
            QMessageBox.information(self, "Success", "Login successful!")
            self.search_form = SearchForm()
            self.search_form.show()
            self.hide()
        else:
            QMessageBox.warning(self, "Error", "Invalid login or password!")

    def open_add_user_form(self):
        self.add_user_form = AddUserForm()
        self.add_user_form.show()


class AddUserForm(BaseForm):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("New User")

        self.layout = QVBoxLayout()

        self.input_name = self.add_label_and_input("Name:")
        self.input_login = self.add_label_and_input("Login:")
        self.input_password = self.add_label_and_input("Password:", is_password=True)

        self.add_button("Add User", self.handle_add_user)
        self.add_button("Exit", self.close)

        self.setLayout(self.layout)

    def handle_add_user(self):
        name = self.input_name.text()
        login = self.input_login.text()
        password = self.input_password.text()

        if name and login and password:
            add_user(name, login, password, self)
        else:
            QMessageBox.warning(self, "Error", "All fields must be filled!")


if __name__ == "__main__":
    initialize_db()
    app = QApplication(sys.argv)
    login_form = LoginForm()
    login_form.show()
    sys.exit(app.exec_())
