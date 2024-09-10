import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QFormLayout, QPushButton,
    QLineEdit, QSpacerItem, QSizePolicy, QLabel, QMessageBox
)
from request import get_token, register  # Импортируем функции из request.py

# Comment window after login/registration
class CommentWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Add a Comment')
        self.setGeometry(100, 100, 400, 300)

        # Layout for the comment form
        self.layout = QVBoxLayout()

        self.comment_input = QLineEdit(self)
        self.layout.addWidget(QLabel('Add your comment:'))
        self.layout.addWidget(self.comment_input)

        # Submit button
        self.submit_button = QPushButton('Submit Comment', self)
        self.submit_button.clicked.connect(self.submit_comment)
        self.layout.addWidget(self.submit_button)

        # Setting layout
        self.setLayout(self.layout)

    def submit_comment(self):
        comment = self.comment_input.text()
        print(f'Comment Submitted: {comment}')
        # Here you can add logic to send the comment somewhere


# Main application for login and registration
class SimpleApp(QWidget):
    def __init__(self):
        super().__init__()

        # Main window for login/signup
        self.setWindowTitle('UsersCrud')
        self.showMaximized()

        # Main layout
        self.main_layout = QVBoxLayout()

        # Creating the form for email and password
        self.form_layout = QFormLayout()

        # Email input
        self.email_input = QLineEdit(self)
        self.form_layout.addRow('Enter your email:', self.email_input)

        # Password input
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)  # Hide input for the password
        self.form_layout.addRow('Enter your password:', self.password_input)

        # Confirm password input (for registration)
        self.confirm_password_input = QLineEdit(self)
        self.confirm_password_input.setEchoMode(QLineEdit.Password)  # Hide input for the password
        self.confirm_password_label = QLabel('Confirm your password:')  # Create label for confirm password
        self.form_layout.addRow(self.confirm_password_label, self.confirm_password_input)
        self.confirm_password_input.hide()  # Initially hidden
        self.confirm_password_label.hide()  # Hide the label as well

        # Add form to main layout
        self.main_layout.addLayout(self.form_layout)

        # Spacer items for centering the form
        spacer_top = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        spacer_bottom = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.main_layout.addItem(spacer_top)

        # Log In/Sign Up button
        self.submit_button = QPushButton('Log In', self)
        self.submit_button.clicked.connect(self.on_submit)
        self.main_layout.addWidget(self.submit_button)

        # Toggle button for switching between login and registration
        self.toggle_button = QPushButton('Register', self)
        self.toggle_button.clicked.connect(self.toggle_form)
        self.main_layout.addWidget(self.toggle_button)

        self.main_layout.addItem(spacer_bottom)

        self.setLayout(self.main_layout)

        self.is_registration = False  # Initially in login mode

    def on_submit(self):
        email = self.email_input.text()
        password = self.password_input.text()

        if self.is_registration:
            # Handle Registration
            confirm_password = self.confirm_password_input.text()

            if password != confirm_password:
                self.show_message('Registration failed!', 'Passwords do not match!')
                return

            success, result = register(email, password, confirm_password)
            if success:
                self.show_message('Registration successful!', result)
                self.toggle_form()  # Switch back to login form after successful registration
            else:
                self.show_message('Registration failed!', result)

        else:
            # Handle Login
            success, token = get_token(email, password)
            if success:
                self.show_message('Login successful!', f'Token: {token}')
                self.open_comment_window()
            else:
                self.show_message('Login failed!', token)

    def toggle_form(self):
        """Toggle between login and registration form."""
        if not self.is_registration:
            # Switch to registration mode
            self.confirm_password_input.show()
            self.confirm_password_label.show()  # Show the label
            self.submit_button.setText('Register')
            self.toggle_button.setText('Log In')
            self.is_registration = True
        else:
            # Switch to login mode
            self.confirm_password_input.hide()  # Hide the confirm password field
            self.confirm_password_label.hide()  # Hide the label
            self.submit_button.setText('Log In')
            self.toggle_button.setText('Register')
            self.is_registration = False

    def open_comment_window(self):
        self.comment_window = CommentWindow()
        self.comment_window.show()

    def show_message(self, title, message):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setText(message)
        msg_box.setWindowTitle(title)
        msg_box.exec_()


def main():
    app = QApplication(sys.argv)
    window = SimpleApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
