from PyQt5 import QtGui
from PyQt5.QtCore import QUrlQuery, Qt
from PyQt5.QtGui import QCursor, QFont, QIcon
from PyQt5.QtWidgets import (
    QApplication,
    QDialog,
    QDialogButtonBox,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QMessageBox,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
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
    get_selected_courseButton_StyleSheet,
    get_nonclickeble_saveButton_StyleSheet
)


class CourseViewWindow(QWidget):
    def __init__(self, courseSender, courseName="englishSlangCourse"):
        super().__init__()
        self.isCourseChecked = courseSender.is_using
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
        # -------------------------------------Окно-------------------------------------
        self.setWindowTitle(self.courseName)
        self.setWindowIcon(QIcon("Icons/appIcon_v3.png"))
        self.move(100, 100)
        self.setMinimumWidth(840)
        self.setMinimumHeight(500)

        self.courseWordsTW = QTableWidget(self)  # Таблица для отображения БД

        # ------------------------------------Кнопки------------------------------------
        self.saveButton = QPushButton("Сохранить изменения", self)
        self.saveButton.clicked.connect(self.saveChanges)
        self.saveButton.setStyleSheet(get_nonclickeble_saveButton_StyleSheet())
        self.saveButton.setFont(QFont("Yu Gothic UI Semibold", 10))
        self.saveButton.setCursor(QCursor(Qt.ForbiddenCursor))
        self.saveButton.isClickable = False

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
        self.statusbar.setText('')

        # ----------------------------------Компоновка----------------------------------
        self.horizontalSpacer = QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum
        )
        
        self.buttonsLayout = QHBoxLayout()
        self.buttonsLayout.addWidget(self.statusbar)
        self.buttonsLayout.addItem(self.horizontalSpacer)
        self.buttonsLayout.addWidget(self.saveButton)
        self.buttonsLayout.addWidget(self.changeViewButton)
        self.buttonsLayout.addWidget(self.addRowButton)
        
        self.globalLayout = QVBoxLayout()
        self.globalLayout.addWidget(self.courseWordsTW)
        self.globalLayout.addLayout(self.buttonsLayout)
        self.setLayout(self.globalLayout)

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

        self.courseWordsTW.itemChanged.connect(self.item_changed)

    def item_changed(self, item):
        """ Если ячейка поменяла значение, то будет вызван этот метод """

        # Если значения поменялись, то добавляем к названию окна *
        wt = self.windowTitle()  
        if '*' not in wt:
            self.setWindowTitle(wt + '*')

        changedColumn = self.translatedTitles[self.titles[item.column()]]  # Переводим 
        #                             колонки в те названия, которые используются в БД

        changedItem = item.text()
        if changedItem:
            # Перевод + и - в «булевые» значения
            if changedItem == "+":
                changedItem = 1
            elif changedItem == "-":
                changedItem = 0
            
            # Добавляем в словарь измененные значения
            self.changed[item.row(), changedColumn] = changedItem
        else:
            # Добавляем в словарь новые значения
            self.added[item.row()] = [
                ('word', 'value', 'is_using'), ('', '', '')
            ]

        # Делаем кнопку кликабельной
        self.saveButton.isClickable = True  
        self.saveButton.setStyleSheet(get_saveButton_StyleSheet())
        self.saveButton.setCursor(QCursor(Qt.PointingHandCursor))

    def saveChanges(self):
        """ Сохранение данных """

        if not self.saveButton.isClickable:  # Если изменений не было, 
            #                                  то кнопка работать не будет
            return
        
        cur = self.con.cursor()
        # Создаем новые строки из словаря новых строк
        for row in self.added.keys():
            query = f"""
                INSERT INTO {self.courseName} {self.added[row][0]}
                VALUES {self.added[row][1]}
            """
            cur.execute(query)
            self.con.commit()

        check = self.__checkCells()  # Проверка ячеек перед сохранением данных
        if check:
            self.statusbar.setText(check)
            return

        # Сохранем данные
        for row, col in self.changed.keys():
            query = f"""
                UPDATE {self.courseName}
                SET {col} = '{self.changed[(row, col)]}'
                WHERE id = {row + 1}
            """
            cur.execute(query)

        self.con.commit()  # Коммит

        # Опустошаем контейнеры
        self.changed = dict()
        self.added = dict()

        # Меняем название окна
        self.setWindowTitle(self.windowTitle()[:-1])

        # Делаем кнопку некликабельной
        self.saveButton.setStyleSheet(get_nonclickeble_saveButton_StyleSheet())
        self.saveButton.setCursor(QCursor(Qt.ForbiddenCursor))
        self.saveButton.isClickable = False
        self.statusbar.setText('')

    def changeView(self):
        """ Изменение отображения таблицы, довольно бесполезный метод но пусть будет """

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
        """ Добавление строки в таблицу. Работает только в myCourse """

        r = self.courseWordsTW.rowCount()
        self.courseWordsTW.setRowCount(r + 1)
        [
            self.courseWordsTW.setItem(r, c, QTableWidgetItem(""))
            for c in range(self.courseWordsTW.columnCount())
        ]
    
        
    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        """ Синхронизация с главным окном и проверка на сохранение данных """

        if self.saveButton.isClickable:
            close = QMessageBox.question(
                self,
                "Подтвердите действия",
                "Есть несохраненные данные",
                QMessageBox.Save | QMessageBox.Close
            )
            if close == QMessageBox.Close:
                event.accept()
            else:
                event.ignore()
        else:
            if self.isCourseChecked:
                self.courseSender.setStyleSheet(get_selected_courseButton_StyleSheet())
            else:
                self.courseSender.setStyleSheet(get_courseButton_StyleSheet())
            self.__delExcessRows()

    def __checkCells(self):
        """ Проверка на верные значения ячеек таблицы """

        self.isCourseChecked = False
        for ir in range(self.courseWordsTW.rowCount()):
            for ic in range(self.courseWordsTW.columnCount()):
                item = self.courseWordsTW.item(ir, ic).text()
                if not bool(item.strip()):
                    return 'Есть пустые поля!'
                if ic == 2 and item not in '+-01':
                    return 'Неверные значения в 3й колонке (+/-)'
                if ic == 2 and item in '+1':
                    self.isCourseChecked = True
    
    def __delExcessRows(self):
        """ Удалить полностью пустые ряды """
        
        cur = self.con.cursor()
        query = f"""
            DELETE FROM {self.courseName}
            WHERE trim(word) = '' AND trim(value) = '' AND trim(is_using) = ''
        """
        cur.execute(query)
        self.con.commit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    my_app = CourseViewWindow()
    my_app.show()
    sys.exit(app.exec_())
