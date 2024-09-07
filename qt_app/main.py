import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QFormLayout, QPushButton, QLineEdit, QSpacerItem, QSizePolicy


class SimpleApp(QWidget):
    def __init__(self):
        super().__init__()

        # Настройки окна
        self.setWindowTitle('UsersCrud')
        self.showMaximized()

        # Основной вертикальный макет
        self.main_layout = QVBoxLayout()

        # Создаем форму для email и password
        self.form_layout = QFormLayout()

        # Поле для ввода email
        self.email_input = QLineEdit(self)
        self.form_layout.addRow('Enter your email:', self.email_input)

        # Поле для ввода пароля
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)  # Скрытие ввода для пароля
        self.form_layout.addRow('Enter your password:', self.password_input)

        # Добавляем форму в основной макет
        self.main_layout.addLayout(self.form_layout)

        # Пространство сверху и снизу для центровки формы
        spacer_top = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        spacer_bottom = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        # Добавляем пространство сверху
        self.main_layout.addItem(spacer_top)

        # Кнопка Submit
        self.submit_button = QPushButton('Submit', self)
        self.submit_button.clicked.connect(self.on_submit)
        self.main_layout.addWidget(self.submit_button)

        # Кнопка Sign Up (добавлена под кнопкой Submit)
        self.signup_button = QPushButton('Sign up', self)
        self.signup_button.clicked.connect(self.on_signup)
        self.main_layout.addWidget(self.signup_button)

        # Добавляем пространство снизу
        self.main_layout.addItem(spacer_bottom)

        # Устанавливаем основной макет в окно
        self.setLayout(self.main_layout)

        # Поле для подтверждения пароля (по умолчанию скрыто)
        self.confirm_password_input = QLineEdit(self)
        self.confirm_password_input.setEchoMode(QLineEdit.Password)

    # Метод для обработки нажатия кнопки Submit
    def on_submit(self):
        email = self.email_input.text()
        password = self.password_input.text()

        # Если форма регистрации (Sign up), проверяем подтверждение пароля
        if self.confirm_password_input.isVisible():
            confirm_password = self.confirm_password_input.text()
            if password != confirm_password:
                print("Пароли не совпадают!")
            else:
                print(f'Registered with Email: {email}, Password: {password}')
        else:
            print(f'Logged in with Email: {email}, Password: {password}')

    # Метод для обработки нажатия кнопки Sign Up
    def on_signup(self):
        # Добавляем поле для подтверждения пароля
        self.form_layout.addRow('Confirm your password:', self.confirm_password_input)
        self.confirm_password_input.show()

        # Меняем текст кнопки Submit на "Register"
        self.submit_button.setText('Register')

        # Скрываем кнопку Sign Up
        self.signup_button.hide()


def main():
    # Создаем приложение
    app = QApplication(sys.argv)

    # Создаем объект окна
    window = SimpleApp()

    # Показываем окно
    window.show()

    # Запускаем цикл обработки событий
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
