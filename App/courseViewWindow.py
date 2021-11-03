from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor, QFont, QIcon
from PyQt5.QtWidgets import QApplication, QHeaderView, QPushButton, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget
import sqlite3
import sys

from style import get_changeViewButton_StyleSheet, get_saveButton_StyleSheet


class CourseViewWindow(QWidget):
    def __init__(self, courseName='englishSlangCourse'):
        super().__init__()
        self.courseName = courseName
        self.translatedTitles = {
            'Слово': 'word',
            'Значение': 'value',
            'Используется': 'is_using'
        }
        self.titles = ['Слово', 'Значение', "Используется"]
        self.setupUi()
        self.setupBackEnd()

    def setupUi(self):
        self.setWindowTitle(self.courseName)
        self.setWindowIcon(QIcon("Icons/appIcon_v3.png"))
        self.setGeometry(100, 100, 700, 500)
        
        self.courseWordsTW = QTableWidget(self)  # Таблица для отображения БД

        # ------------------------------------Кнопки------------------------------------
        self.saveButton = QPushButton('Сохранить изменения', self)
        self.saveButton.clicked.connect(self.saveChanges)
        self.saveButton.setStyleSheet(get_saveButton_StyleSheet())
        self.saveButton.setFont(QFont("Yu Gothic UI Semibold", 10))
        self.saveButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.saveButton.hide()

        self.changeViewButton = QPushButton('Изменить отображение', self)
        self.changeViewButton.clicked.connect(self.changeView)
        self.changeViewButton.isChanged = False
        self.changeViewButton.setStyleSheet(get_changeViewButton_StyleSheet())
        self.changeViewButton.setFont(QFont("Yu Gothic UI Semibold", 10))
        self.changeViewButton.setCursor(QCursor(Qt.PointingHandCursor))
        
        # ----------------------------------Компоновка----------------------------------
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.courseWordsTW)
        self.layout.addWidget(self.changeViewButton)
        self.layout.addWidget(self.saveButton)
        self.setLayout(self.layout)

    def setupBackEnd(self):
        self.changed = dict()  # Здесь будут временно храниться изменения

        self.con = sqlite3.connect('WordsDB/words.db')
        cur = self.con.cursor()
        query = f"""
            SELECT word, value, is_using FROM {self.courseName}
        """
        res = cur.execute(query).fetchall()

        # -----------------------------Отображение таблицы------------------------------
        self.courseWordsTW.setRowCount(len(res))
        self.courseWordsTW.setColumnCount(3)
        self.courseWordsTW.setHorizontalHeaderLabels(self.titles)
        for ir, row in enumerate(res):
            for ic, item in enumerate(row):
                if ic == 2:
                    item = '+' if item else '-'
                self.courseWordsTW.setItem(ir, ic, QTableWidgetItem(str(item)))

        self.changeView()
        self.courseWordsTW.itemChanged.connect(self.item_changed)

    def item_changed(self, item):
        changedColumn = self.translatedTitles[self.titles[item.column()]]
        changedItem = item.text()
        if changedItem == '+':
            changedItem = 1
        elif changedItem == '-':
            changedItem = 0
        self.changed[changedColumn] = changedItem

        self.saveButton.show()
    
    def saveChanges(self):
        cur = self.con.cursor()
        query = f"UPDATE {self.courseName} SET\n"
        query += ', '.join(f"{key} = {self.changed.get(key, 'err')}" for key in self.changed.keys())
        cur.execute(query)
        self.con.commit()

        self.changed = dict()
        self.saveButton.hide()
    
    def changeView(self):
        if not self.changeViewButton.isChanged:
            self.courseWordsTW.resizeColumnsToContents()
            self.changeViewButton.isChanged = True
        else:
            for i in range(len(self.titles)):
                self.courseWordsTW.horizontalHeader().resizeSection(i, 100)
            self.changeViewButton.isChanged = False

        self.courseWordsTW.horizontalHeader().setSectionResizeMode(
            2, QHeaderView.Stretch
        )


if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_app = CourseViewWindow()
    my_app.show()
    sys.exit(app.exec_())