import sys

from PyQt6.QtWidgets import (QApplication, QLabel, QWidget,
                             QGridLayout, QLineEdit, QPushButton)
from datetime import datetime


class AgeCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Age Calculator")
        # adding grid layout

        grid = QGridLayout()

        name_label = QLabel("Name:")
        self.name_line_edit = QLineEdit()

        dob_label = QLabel("Date of Birth DD/MM/YYYY:")
        self.date_of_birth_line_edit = QLineEdit()

        calculate_button = QPushButton("Calculate")
        calculate_button.clicked.connect(self.calculate_age)

        self.output_label = QLabel("")

        # Adding widgets to grid
        grid.addWidget(name_label, 0, 0)
        grid.addWidget(self.name_line_edit, 0, 1)
        grid.addWidget(dob_label, 1, 0)
        grid.addWidget(self.date_of_birth_line_edit, 1, 1)
        grid.addWidget(calculate_button, 0, 2, 2, 1)
        grid.addWidget(self.output_label, 3, 0, 2, 1)

        # self is creating an instance 
        self.setLayout(grid)

    def calculate_age(self):
        try:
            current_year = datetime.now().year
            date_of_birth = self.date_of_birth_line_edit.text()
            year_of_birth = datetime.strptime(date_of_birth, "%d/%m/%Y").date().year
            age = current_year - year_of_birth
            name = self.name_line_edit.text()
            self.output_label.setText(f"{name} is  {age} years old.")

        except ValueError:
            self.output_label.setText("Please enter the date in MM/DD/YYYY format.")


# main loop


app = QApplication(sys.argv)
age_calculator = AgeCalculator()
age_calculator.show()
sys.exit(app.exec())
