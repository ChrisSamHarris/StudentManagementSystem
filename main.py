from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QVBoxLayout, QLabel, QWidget, QGridLayout, \
    QLineEdit, QPushButton, QMainWindow, QTableWidget, QTableWidgetItem, QDialog, QBoxLayout, \
    QComboBox, QVBoxLayout
from PyQt6.QtGui import QAction
import sys
import sqlite3

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")
        self.setFixedWidth(600)
        self.setFixedHeight(600)
        
        file_menu_item = self.menuBar().addMenu("&File")
        add_student_action = QAction("Add Student", self)
        file_menu_item.addAction(add_student_action)
        add_student_action.triggered.connect(self.insert)
        
        
        help_menu_item = self.menuBar().addMenu("&Help")
        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)
        about_action.setMenuRole(QAction.MenuRole.NoRole)
        
        edit_menu_item = self.menuBar().addMenu("&Edit")
        edit_action = QAction("Search", self)
        edit_menu_item.addAction(edit_action)
        edit_action.triggered.connect(self.search)
        
        
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("Id", "Name", "Course", "Mobile"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)
        
    def load_data(self):
        connection = sqlite3.connect("database/database.db")
        result = connection.execute("SELECT * FROM students")
        # print(list(result))
        
        # Result the table and load the table as fresh to stop overwrites and duplicates:
        self.table.setRowCount(0)
        
        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        connection.close()
        
    def insert(self):
        dialog = InsertDialog()
        dialog.exec()
        
    def search(self):
        dialog = SearchDialog()
        dialog.exec()
        
        
class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Insert Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)
            
        layout = QVBoxLayout()
        
        # Student Layout Widgets
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("John Smith")
        layout.addWidget(self.student_name)
        
        # Combo box of courses
        self.course_name = QComboBox()
        courses = ["Biology", "Math", "Astronomy", "Physics"]
        self.course_name.addItems(courses)
        layout.addWidget(self.course_name)
        
        # Add Mobile Widget
        self.mobile = QLineEdit()
        self.mobile.setPlaceholderText("1122334455")
        layout.addWidget(self.mobile)
        
        # Submit Button
        button = QPushButton("Register")
        button.clicked.connect(self.add_student)
        layout.addWidget(button)
        
        self.setLayout(layout)
        
    def add_student(self):
        name = self.student_name.text()
        course = self.course_name.itemText(self.course_name.currentIndex())
        mobile = self.mobile.text()
        
        connection = sqlite3.connect("database/database.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO students (name, course, mobile) VALUES (?,?,?)",
                       (name, course, mobile))
        connection.commit()
        cursor.close()
        connection.close()
        student_mgmt.load_data()
        
class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Search Student")
        self.setFixedWidth(300)
        self.setFixedHeight(300)
            
        layout = QVBoxLayout()
        
        # Search Layout Widgets
        self.search_name = QLineEdit()
        self.search_name.setPlaceholderText("Student Name")
        layout.addWidget(self.search_name)
        
        # Submit Button
        button = QPushButton("Search")
        button.clicked.connect(self.search_funct)
        layout.addWidget(button)
        
        self.setLayout(layout)
        
    def search_funct(self):
        name = self.search_name.text()
        connection = sqlite3.connect("database/database.db")
        cursor = connection.cursor()
        result = cursor.execute("SELECT * FROM students WHERE name = ?", (name,))
        rows = list(result)
        print(rows)
        items = student_mgmt.table.findItems(name, Qt.MatchFlag.MatchFixedString)
        for item in items:
            print(item)
            student_mgmt.table.item(item.row(), 1).setSelected(True)
            
        cursor.close()
        connection.close()
        

app = QApplication(sys.argv)
student_mgmt = MainWindow()
student_mgmt.show()
student_mgmt.load_data()
sys.exit(app.exec())