import sys
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QFormLayout, QPushButton,
    QLineEdit, QSpacerItem, QSizePolicy, QLabel, QMessageBox, QListWidget
)
from request import get_token, register, get_active_users, get_comments, add_comment



class CommentWindow(QWidget):
    def __init__(self, token):
        super().__init__()
        self.token = token
        self.setWindowTitle('Comments')
        self.showMaximized()

        self.layout = QVBoxLayout()
        self.active_users_list = QListWidget()
        self.layout.addWidget(QLabel('Active Users:'))
        self.layout.addWidget(self.active_users_list)
        self.load_active_users()

        self.comments_list = QListWidget()
        self.layout.addWidget(QLabel('Comments:'))
        self.layout.addWidget(self.comments_list)
        self.load_comments()

        self.comment_input = QLineEdit(self)
        self.layout.addWidget(QLabel('Add your comment:'))
        self.layout.addWidget(self.comment_input)

        self.submit_button = QPushButton('Submit Comment', self)
        self.submit_button.clicked.connect(self.submit_comment)
        self.layout.addWidget(self.submit_button)

        self.setLayout(self.layout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.load_comments)
        self.timer.start(10000)

    def load_active_users(self):
        try:
            active_users = get_active_users(self.token)
            self.active_users_list.addItems(active_users)
        except Exception as e:
            print(f"Error loading active users: {e}")
            self.active_users_list.addItem("Failed to load active users")

    def load_comments(self):
        try:
            comments = get_comments(self.token)
            self.comments_list.clear()
            for comment in comments:
                self.comments_list.addItem(f"({comment.get('creator_email')}): {comment.get('comment')}")
        except Exception as e:
            print(f"Error loading comments: {e}")
            self.comments_list.addItem("Failed to load comments")

    def submit_comment(self):
        comment = self.comment_input.text()
        if not comment.strip():
            self.show_message('Comment Error', 'Comment cannot be empty!')
            return
        
        try:
            response = add_comment(self.token, comment)
            if response.get('comment') == comment:
                self.comments_list.addItem(f"You: {comment}")
                self.comment_input.clear()
            else:
                self.show_message('Submission Error', 'Failed to submit comment!')
        except Exception as e:
            print(f"Error submitting comment: {e}")
            self.show_message('Submission Error', 'An error occurred while submitting the comment.')

    def show_message(self, title, message):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setText(message)
        msg_box.setWindowTitle(title)
        msg_box.exec_()


class SimpleApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('UsersCrud')
        self.showMaximized()

        self.main_layout = QVBoxLayout()

        self.form_layout = QFormLayout()


        self.email_input = QLineEdit(self)
        self.form_layout.addRow('Enter your email:', self.email_input)

        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)
        self.form_layout.addRow('Enter your password:', self.password_input)

        self.confirm_password_input = QLineEdit(self)
        self.confirm_password_input.setEchoMode(QLineEdit.Password) 
        self.confirm_password_label = QLabel('Confirm your password:') 
        self.form_layout.addRow(self.confirm_password_label, self.confirm_password_input)
        self.confirm_password_input.hide()  
        self.confirm_password_label.hide()  


        self.main_layout.addLayout(self.form_layout)

 
        spacer_top = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        spacer_bottom = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.main_layout.addItem(spacer_top)

     
        self.submit_button = QPushButton('Log In', self)
        self.submit_button.clicked.connect(self.on_submit)
        self.main_layout.addWidget(self.submit_button)

        
        self.toggle_button = QPushButton('Register', self)
        self.toggle_button.clicked.connect(self.toggle_form)
        self.main_layout.addWidget(self.toggle_button)

        self.main_layout.addItem(spacer_bottom)

        self.setLayout(self.main_layout)

        self.is_registration = False 

    def on_submit(self):
        email = self.email_input.text()
        password = self.password_input.text()

        if self.is_registration:
           
            confirm_password = self.confirm_password_input.text()

            if password != confirm_password:
                self.show_message('Registration failed!', 'Passwords do not match!')
                return

            success, result = register(email, password, confirm_password)
            if success:
                self.show_message('Registration successful!', result)
                self.toggle_form()  
            else:
                self.show_message('Registration failed!', result)

        else:
            
            success, token = get_token(email, password)
            if success:
                self.show_message('Login successful!', f'Token: {token}')
                self.open_comment_window(token) 
            else:
                self.show_message('Login failed!', token)

    def toggle_form(self):
        """Toggle between login and registration form."""
        if not self.is_registration:
            
            self.confirm_password_input.show()
            self.confirm_password_label.show() 
            self.submit_button.setText('Register')
            self.toggle_button.setText('Log In')
            self.is_registration = True
        else:
            
            self.confirm_password_input.hide()  
            self.confirm_password_label.hide()  
            self.submit_button.setText('Log In')
            self.toggle_button.setText('Register')
            self.is_registration = False

    def open_comment_window(self, token):
        """ """
        self.comment_window = CommentWindow(token)
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