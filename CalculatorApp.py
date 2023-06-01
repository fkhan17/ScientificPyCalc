import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QPushButton, QVBoxLayout, QWidget, QGridLayout, QStatusBar
from PyQt5.QtCore import Qt
import math


class Calculator(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Calculator App")
        self.setGeometry(100, 100, 300, 400)
        self.setStyleSheet(
            "background-color: #F0F0F0; border: 1px solid #C0C0C0;")
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        self.result_line_edit = QLineEdit()
        layout.addWidget(self.result_line_edit)
        self.result_line_edit.setMinimumHeight(100)
        self.result_line_edit.setStyleSheet("""
            background-color: #FFFFFF;
            border: 1px solid #C0C0C0;
            color: #000000;
            font: 38pt "Arial";
            padding: 5px;
            margin: 10px;
""")

        grid_layout = QGridLayout()
        layout.addLayout(grid_layout)

        buttons = [
            ("7", 0, 0), ("8", 0, 1), ("9", 0, 2), ("/", 0, 3),
            ("4", 1, 0), ("5", 1, 1), ("6", 1, 2), ("*", 1, 3),
            ("1", 2, 0), ("2", 2, 1), ("3", 2, 2), ("-", 2, 3),
            ("0", 3, 0), (".", 3, 1), ("+", 3, 2), ("=", 3, 3)
        ]

        adv_buttons = [
            ("C", 0, 4), ("MC", 1, 4), ("MR", 2, 4), ("M+", 3, 4), ("M-", 4, 4),
            ("sin", 0, 5), ("cos", 1, 5), ("tan",
                                           2, 5), ("log", 3, 5), ("sqrt", 4, 5),
        ]
        number_button_style = """
            QPushButton {
                background-color: #E0E0E0;
                border: 1px solid #C0C0C0;
                color: #000000;
                font: 22pt "Arial";
                padding: 5px;
                margin: 5px;
                min-width: 60px;
                min-height: 60px;
            }
            QPushButton:hover {
                background-color: #F0F0F0;
            }
            QPushButton:pressed {
                background-color: #D0D0D0;
            }
        """

        operator_button_style = """
            QPushButton {
                background-color: #F0A030;
                border: 1px solid #C0C0C0;
                color: #000000;
                font: 22pt "Arial";
                padding: 5px;
                margin: 5px;
                min-width: 60px;
                min-height: 60px;
            }
            QPushButton:hover {
                background-color: #F0C060;
            }
            QPushButton:pressed {
                background-color: #D09030;
            }
        """

        function_button_style = """
            QPushButton {
                background-color: #B0B0B0;
                border: 1px solid #C0C0C0;
                color: #000000;
                font:22pt "Arial";
                padding: 5px;
                margin: 5px;
                min-width: 60px;
                min-height: 60px;
            }
            QPushButton:hover {
                background-color: #C0C0C0;
            }
            QPushButton:pressed {
                background-color: #A0A0A0;
            }
        """

        for (text, row, col) in buttons + adv_buttons:
            button = QPushButton(text)
            if text.isdigit() or text == ".":
                button.setStyleSheet(number_button_style)
            elif text in ("+", "-", "*", "/"):
                button.setStyleSheet(operator_button_style)
            else:
                button.setStyleSheet(function_button_style)

            if text in ("C", "MC", "MR", "M+", "M-", "sin", "cos", "tan", "log", "sqrt"):
                button.clicked.connect(
                    lambda _, t=text: self.on_adv_button_click(t))
            else:
                button.clicked.connect(
                    lambda _, t=text: self.on_button_click(t))

            grid_layout.addWidget(button, row, col)

        # Status bar for error messages
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

    def on_button_click(self, text):
        if text == "=":
            try:
                expression = self.result_line_edit.text()
                result = eval(expression)
                self.result_line_edit.setText(str(result))
            except Exception as e:
                self.result_line_edit.setText("Error")
        else:
            current_text = self.result_line_edit.text()
            self.result_line_edit.setText(current_text + text)

    def on_adv_button_click(self, text):
        current_text = self.result_line_edit.text()

        if text == "C":
            self.result_line_edit.clear()
        elif text in ("MC", "MR", "M+", "M-"):
            self.handle_memory_operations(text)
        else:
            try:
                value = float(current_text)
                if text == "sin":
                    result = math.sin(math.radians(value))
                elif text == "cos":
                    result = math.cos(math.radians(value))
                elif text == "tan":
                    result = math.tan(math.radians(value))
                elif text == "log":
                    result = math.log(value)
                elif text == "sqrt":
                    result = math.sqrt(value)
                self.result_line_edit.setText(str(result))
            except ValueError:
                self.status_bar.showMessage(
                    "Invalid input for advanced operations", 3000)

    def handle_memory_operations(self, operation):
        if operation == "MC":
            self.memory = 0
        elif operation == "MR":
            self.result_line_edit.setText(str(self.memory))
        elif operation == "M+":
            try:
                value = float(self.result_line_edit.text())
                self.memory += value
            except ValueError:
                self.status_bar.showMessage(
                    "Invalid input for memory operation", 3000)
        elif operation == "M-":
            try:
                value = float(self.result_line_edit.text())
                self.memory -= value
            except ValueError:
                self.status_bar.showMessage(
                    "Invalid input for memory operation", 3000)

    def keyPressEvent(self, event):
        key = event.key()

        if key >= Qt.Key_0 and key <= Qt.Key_9:
            self.result_line_edit.setText(
                self.result_line_edit.text() + str(key - Qt.Key_0))
        elif key in (Qt.Key_Plus, Qt.Key_Minus, Qt.Key_Asterisk, Qt.Key_Slash):
            self.result_line_edit.setText(
                self.result_line_edit.text() + event.text())
        elif key == Qt.Key_Backspace:
            self.result_line_edit.backspace()
        elif key == Qt.Key_Return or key == Qt.Key_Enter:
            self.on_button_click("=")
        elif key == Qt.Key_Escape:
            self.result_line_edit.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    calculator = Calculator()
    calculator.memory = 0
    calculator.show()
    sys.exit(app.exec_())
