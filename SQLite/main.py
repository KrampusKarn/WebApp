import sys
import sqlite3

from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import (QApplication, QMainWindow, QTableWidget, QDialog, QVBoxLayout, QLineEdit, QTableWidgetItem,
                             QComboBox, QPushButton, QToolBar, QStatusBar, QLabel, QGridLayout, QMessageBox)


class DatabaseConnection:
    def __init__(self, database_file="database.db"):
        self.database_file = database_file

    def connect(self):
        connection = sqlite3.connect(self.database_file)
        return connection


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")
        self.setMinimumSize(800, 600)

        # menu bar
        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")
        edit_menu_item = self.menuBar().addMenu("&Edit")
        tools_menu_item = self.menuBar().addMenu("&Tools")

        # add student action in the file
        add_student_action = QAction("Add Student", self)
        add_student_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_student_action)

        # add tools action
        attendance_action = QAction("Track Attendance", self)
        attendance_action.triggered.connect(self.track_attendance)
        tools_menu_item.addAction(attendance_action)

        # add report action
        report_action = QAction("Report")
        report_action.triggered.connect(self.report)

        # about the db
        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)
        about_action.setMenuRole(QAction.MenuRole.NoRole)
        about_action.triggered.connect(self.about)

        # search for particular student
        search_action = QAction("Search", self)
        edit_menu_item.addAction(search_action)
        search_action.triggered.connect(self.search)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("Id", "Name", "Course", "Mobile"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

        toolbar = QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)
        toolbar.addAction(add_student_action)
        toolbar.addAction(search_action)

        # create a status bar
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

        self.table.cellClicked.connect(self.cell_clicked)

        # message
        latest_update = QLabel("Check out new Students registration")
        self.statusbar.addWidget(latest_update)

    def cell_clicked(self):
        edit_button = QPushButton("Edit Record")
        edit_button.clicked.connect(self.edit)

        delete_button = QPushButton("Delete Record")
        delete_button.clicked.connect(self.delete)

        children = self.findChildren(QPushButton)
        if children:
            for child in children:
                self.statusbar.removeWidget(child)

        self.statusbar.addWidget(edit_button)
        self.statusbar.addWidget(delete_button)

    def load_data(self):
        self.table.setRowCount(0)  # clear table after loading
        connection = sqlite3.connect("database.db")
        result = connection.execute("SELECT * FROM students")
        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        connection.close()

    def insert(self):
        dialog = InsertDialog()
        dialog.exec()

    def search(self):
        dialog = SearchDialog(self)
        dialog.exec()

    def clear_search(self):
        self.table.setRowCount(0)
        self.load_data()

    def edit(self):
        index = self.table.currentRow()  # get the current row
        if index != -1:
            dialog = EditDialog(index)  # pass index
            dialog.exec()

    def delete(self):
        dialog = DeleteDialog()
        dialog.exec()

    # waiting for logic
    def track_attendance(self):
        pass

    # waiting for logic
    def report(self):
        pass

    def about (self):
        dialog = AboutDialog()
        dialog.exec()


class AboutDialog(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About")
        content = """
        This is a demo database project, Student Information Management System that I used to learn more about 
        Python Libraries, OOP and other operations.
        """
        self.setText(content)


class EditDialog(QDialog):
    def __init__(self, index):
        super().__init__()
        self.index = index
        self.setWindowTitle("Update Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        # Get the student data from the table using the index I defined
        index = main_window.table.currentRow()
        student_name = main_window.table.item(self.index, 1).text()

        # get id from selected row
        self.student_id = main_window.table.item(index, 0).text()

        self.student_name = QLineEdit(student_name)
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        # combo button edit
        course_name = main_window.table.item(self.index, 2).text()
        self.course_name = QComboBox()
        courses = ["Biology", "Math", "English", "Physics", "Chemistry"]
        self.course_name.addItems(courses)
        self.course_name.setCurrentText(course_name)
        layout.addWidget(self.course_name)

        # mobile button
        mobile = main_window.table.item(self.index, 3).text()
        self.mobile = QLineEdit(mobile)
        self.mobile.setPlaceholderText("Mobile")
        layout.addWidget(self.mobile)

        # Add the "update" button
        button = QPushButton("Update")
        button.clicked.connect(self.update_student)
        layout.addWidget(button)

        self.setLayout(layout)

    def update_student(self):
        # Get updated data from the input fields
        new_name = self.student_name.text()
        new_course = self.course_name.currentText()
        new_mobile = self.mobile.text()

        # Get the ID of the student to update
        student_id = main_window.table.item(self.index, 0).text()

        # Update the database
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("UPDATE students SET name = ?, course = ?, mobile = ? WHERE id = ?",
                       (new_name, new_course, new_mobile, student_id))
        connection.commit()
        cursor.close()
        connection.close()

        # Refresh the table to show the updated data
        main_window.load_data()

        # Close the dialog after updating
        self.close()


class DeleteDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Delete Student Data")

        layout = QGridLayout()
        confirmation = QLabel("Are you sure you want to delete?")
        yes = QPushButton("Yes")
        no = QPushButton("No")

        layout.addWidget(confirmation, 0, 0, 1, 2)
        layout.addWidget(yes, 1, 0)
        layout.addWidget(no, 1, 1)
        self.setLayout(layout)

        yes.clicked.connect(self.accept_delete)
        no.clicked.connect(self.reject_delete)

    def accept_delete(self):
        index = main_window.table.currentRow()
        student_id = main_window.table.item(index, 0).text()

        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("DELETE from students WHERE id = ?", (student_id,))
        connection.commit()
        cursor.close()
        connection.close()
        main_window.load_data()

        self.close()

        confirmation_widget = QMessageBox()
        confirmation_widget.setWindowTitle("Success")
        confirmation_widget.setText("Record was successfully deleted")
        confirmation_widget.exec()

    def reject_delete(self):
        pass


class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Insert Student Data")
        self.setFixedWidth(500)
        self.setFixedHeight(500)

        layout = QVBoxLayout()

        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        #  Name Input with QCompleter
        self.course_name = QComboBox()
        self.course_name.setPlaceholderText("Course Name")
        courses = ["Biology", "Math", "English", "Physics", "Chemistry"]
        self.course_name.addItems(courses)
        # completer = QCompleter(courses)
        # completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        # self.course_name.setCompleter(completer)
        layout.addWidget(self.course_name)

        # add mobile widget
        self.mobile = QLineEdit()
        self.mobile.setPlaceholderText("Mobile")
        layout.addWidget(self.mobile)

        # add input button
        add_button = QPushButton("Add Student")
        add_button.clicked.connect(self.add_student)
        layout.addWidget(add_button)

        self.setLayout(layout)

    def add_student(self):
        name = self.student_name.text()
        course = self.course_name.itemText(self.course_name.currentIndex())
        mobile = self.mobile.text()
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO students (name, course, mobile) VALUES (?, ?, ?)",
                       (name, course, mobile))
        connection.commit()
        cursor.close()
        connection.close()
        main_window.load_data()


class SearchDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Search Students")
        self.setFixedWidth(400)
        self.setFixedHeight(200)

        layout = QVBoxLayout()
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        search_button = QPushButton("Search")
        search_button.clicked.connect(self.search)
        layout.addWidget(search_button)

        clear_button = QPushButton("Clear Search")
        clear_button.clicked.connect(self.clear_search)
        layout.addWidget(clear_button)

        self.setLayout(layout)

    def search(self):
        # Get the search term and clean it
        search_term = self.student_name.text().strip()

        if not search_term:
            # If the search term is empty, clear the table
            self.clear_table()
            status_message = "No search term provided."
            self.update_status_message(status_message)
            return

        # Connect to the database
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()

        try:
            # Perform a case-insensitive search with wildcards
            query = "SELECT * FROM students WHERE name LIKE ?"
            cursor.execute(query, (f"%{search_term}%",))
            rows = cursor.fetchall()

            # Update the table with search results
            self.update_table(rows)

            status_message = f"Found {len(rows)} record(s)."
            self.update_status_message(status_message)

        except sqlite3.Error as e:
            # Handle database errors
            status_message = f"Database error: {e}"
            self.update_status_message(status_message)

        finally:
            # Ensure resources are released
            cursor.close()
            connection.close()

    def clear_search(self):
        parent_window = self.parent()
        if isinstance(parent_window, MainWindow):
            parent_window.clear_search()

    def update_status_message(self, message):
        """Update the status message based on the parent window's status bar or print to console."""
        """Update the status message based on the parent window's status bar or print to console."""
        parent_window = self.parent()
        if isinstance(parent_window, QMainWindow):
            parent_window.statusBar().showMessage(message)
        else:
            print(message)

    def update_table(self, rows):
        # Ensure the parent window and table are accessible
        self.clear_table()
        parent_window = self.parent()
        if isinstance(parent_window, MainWindow):
            table = parent_window.table
            for row_number, row_data in enumerate(rows):
                table.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    table.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        else:
            print("Parent window or table not found.")

    def clear_table(self):
        parent_window = self.parent()
        if isinstance(parent_window, MainWindow):
            table = parent_window.table
            table.setRowCount(0)
        else:
            print("Parent window or table not found.")


app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
main_window.load_data()
sys.exit(app.exec())
