import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QFormLayout, QPushButton, QLineEdit, QSpacerItem, QSizePolicy, QLabel, QMessageBox
from request import get_token, get_active_users, register

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

        # Add form to main layout
        self.main_layout.addLayout(self.form_layout)

        # Spacer items for centering the form
        spacer_top = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        spacer_bottom = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.main_layout.addItem(spacer_top)

        # Log In button
        self.login_button = QPushButton('Log In', self)
        self.login_button.clicked.connect(self.on_login)
        self.main_layout.addWidget(self.login_button)

        # Sign Up button
        self.signup_button = QPushButton('Sign Up', self)
        self.signup_button.clicked.connect(self.on_signup)
        self.main_layout.addWidget(self.signup_button)

        self.main_layout.addItem(spacer_bottom)

        self.setLayout(self.main_layout)

    def on_login(self):
        email = self.email_input.text()
        password = self.password_input.text()

        success, token = get_token(email, password)
        if success:
            self.show_message('Login successful!', f'Token: {token}')
            self.open_comment_window()
        else:
            self.show_message('Login failed!', token)

    def on_signup(self):
        # Show confirm password field when signing up
        if not self.confirm_password_input.isVisible():
            self.form_layout.addRow('Confirm your password:', self.confirm_password_input)
            self.confirm_password_input.show()
        else:
            email = self.email_input.text()
            password = self.password_input.text()
            confirm_password = self.confirm_password_input.text()

            if password != confirm_password:
                self.show_message('Registration failed!', 'Passwords do not match!')
            else:
                success, result = register(email, password, confirm_password)
                if success:
                    self.show_message('Registration successful!', result)
                    self.open_comment_window()
                else:
                    self.show_message('Registration failed!', result)

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
