from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor, QFont, QIcon
from PyQt5.QtWidgets import (
    QApplication,
    QHeaderView,
    QLabel,
    QPushButton,
    QStatusBar,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

import sqlite3
import sys

from style import (
    get_changeViewButton_StyleSheet,
    get_saveButton_StyleSheet,
    get_addRowButton_StyleSheet,
    get_courseButton_StyleSheet,
    get_selected_courseButton_StyleSheet
)


class CourseViewWindow(QWidget):
    def __init__(self, courseSender, courseName="englishSlangCourse"):
        super().__init__()
        self.courseSender = courseSender
        self.courseName = courseName
        self.translatedTitles = {
            "Слово": "word",
            "Значение": "value",
            "Используется": "is_using",
        }
        self.titles = ["Слово", "Значение", "Используется"]
        self.setupUi()
        self.setupBackEnd()

    def setupUi(self):
        self.setWindowTitle(self.courseName)
        self.setWindowIcon(QIcon("Icons/appIcon_v3.png"))
        self.setGeometry(100, 100, 700, 500)

        self.courseWordsTW = QTableWidget(self)  # Таблица для отображения БД

        # ------------------------------------Кнопки------------------------------------
        self.saveButton = QPushButton("Сохранить изменения", self)
        self.saveButton.clicked.connect(self.saveChanges)
        self.saveButton.setStyleSheet(get_saveButton_StyleSheet())
        self.saveButton.setFont(QFont("Yu Gothic UI Semibold", 10))
        self.saveButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.saveButton.hide()

        self.changeViewButton = QPushButton("Изменить отображение", self)
        self.changeViewButton.clicked.connect(self.changeView)
        self.changeViewButton.isChanged = False
        self.changeViewButton.setStyleSheet(get_changeViewButton_StyleSheet())
        self.changeViewButton.setFont(QFont("Yu Gothic UI Semibold", 10))
        self.changeViewButton.setCursor(QCursor(Qt.PointingHandCursor))

        self.addRowButton = QPushButton("Добавить строку", self)
        self.addRowButton.clicked.connect(self.addRow)
        self.addRowButton.setStyleSheet(get_addRowButton_StyleSheet())
        self.addRowButton.setFont(QFont("Yu Gothic UI Semibold", 10))
        self.addRowButton.setCursor(QCursor(Qt.PointingHandCursor))
        if self.courseName != 'myCourse':
            self.addRowButton.hide()

        # ----------------------------------Статус бар----------------------------------
        self.statusbar = QLabel(self)
        self.statusbar.setFont(QFont("Yu Gothic UI Semibold", 8))
        self.statusbar.hide()

        # ----------------------------------Компоновка----------------------------------
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.courseWordsTW)
        self.layout.addWidget(self.saveButton)
        self.layout.addWidget(self.changeViewButton)
        self.layout.addWidget(self.addRowButton)
        self.layout.addWidget(self.statusbar, alignment=Qt.AlignLeft)
        self.setLayout(self.layout)

    def setupBackEnd(self):
        self.changed = dict()  # Здесь будут временно храниться изменения
        self.added = dict()  # Здесь будут временно храниться добавленные строки

        self.con = sqlite3.connect("WordsDB/words.db")
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
                    item = "+" if item else "-"
                self.courseWordsTW.setItem(ir, ic, QTableWidgetItem(str(item)))

        self.changeView()
        self.courseWordsTW.itemChanged.connect(self.item_changed)

    def item_changed(self, item):
        changedColumn = self.translatedTitles[self.titles[item.column()]]
        changedItem = item.text()
        if changedItem:
            if changedItem == "+":
                changedItem = 1
            elif changedItem == "-":
                changedItem = 0
            self.changed[item.row(), changedColumn] = changedItem
        else:
            self.added[item.row()] = [
                ('word', 'value', 'is_using'), ('', '', '')
            ]

        self.saveButton.show()

    def saveChanges(self):
        cur = self.con.cursor()
        for row in self.added.keys():
            query = f"""
                INSERT INTO {self.courseName} {self.added[row][0]}
                VALUES {self.added[row][1]}
            """
            cur.execute(query)
            self.con.commit()

        check = self.__checkCells()
        if check:
            self.statusbar.setText(check)
            self.statusbar.show()
            return

        for row, col in self.changed.keys():
            query = f"""
                UPDATE {self.courseName}
                SET {col} = '{self.changed[(row, col)]}'
                WHERE id = {row + 1}
            """
            cur.execute(query)
        self.con.commit()
        self.changed = dict()
        self.added = dict()
        self.saveButton.hide()
        self.statusbar.hide()

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

    def addRow(self):
        r = self.courseWordsTW.rowCount()
        self.courseWordsTW.setRowCount(r + 1)
        [
            self.courseWordsTW.setItem(r, c, QTableWidgetItem(""))
            for c in range(self.courseWordsTW.columnCount())
        ]
    
    def __checkCells(self):
        self.isCourseChecked = False
        for ir in range(self.courseWordsTW.rowCount()):
            for ic in range(self.courseWordsTW.columnCount()):
                item = self.courseWordsTW.item(ir, ic).text()
                if not bool(item):
                    return 'Есть пустые поля!'
                if ic == 2 and item not in '+-01':
                    return 'Неверные значения в 3й колонке (+/-)'
                if ic == 2 and item in '+1':
                    self.isCourseChecked = True
        
    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        self.__checkCells()
        if self.isCourseChecked:
            self.courseSender.setStyleSheet(get_selected_courseButton_StyleSheet())
        else:
            self.courseSender.setStyleSheet(get_courseButton_StyleSheet())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    my_app = CourseViewWindow()
    my_app.show()
    sys.exit(app.exec_())
