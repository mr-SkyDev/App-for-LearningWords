import sys
import sqlite3

from PyQt5.QtCore import QObject, QRect, QSize, Qt
from PyQt5.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QPushButton,
    QSizePolicy,
    QWidget,
    QGridLayout,
    QVBoxLayout,
    QSpacerItem,
)
from PyQt5.QtGui import QCursor, QFont, QIcon

from style import *  # Стили для виджетов
from settingsWindow import SettingsWindow


class CourseButton(QWidget):
    def __init__(
        self,
        parent,
        name,
        is_using,
        title="Курс",
        complexity="Сложность",
        description="Описание",
    ):
        super().__init__()

        # Кнопка курса
        self.courseButton = QPushButton(parent)
        self.courseButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.courseButton.setFixedSize(400, 150)
        self.courseButton.setStyleSheet(
            get_courseButton_StyleSheet()
            if is_using == 0
            else get_selected_courseButton_StyleSheet()
        )
        self.courseButton.is_using = is_using
        self.courseButton.is_courseButton = True
        self.courseButton.name = name

        # Название курса
        self.title = QLabel(
            title, self.courseButton, objectName="CourseButton-TitleLabel"
        )
        self.title.move(10, 10)
        self.title.setStyleSheet(get_courseButton_titleLabel_StyleSheet())

        # Сложность курса
        self.complexity = QLabel(
            complexity, self.courseButton, objectName="CourseButton-ComplexityLabel"
        )
        self.complexity.move(10, 27)
        self.complexity.setStyleSheet(get_courseButton_complexityLabel_StyleSheet())

        # Описание курса
        self.description = QLabel(
            description,
            self.courseButton,
            objectName="CourseButton-DescriptionLabel",
        )
        self.description.move(10, 127)
        self.description.setStyleSheet(get_courseButton_descriptionLabel_StyleSheet())


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("App for LearningWords")
        self.setGeometry(300, 300, 700, 700)
        self.setWindowIcon(QIcon("Icons/appIcon_v3.png"))

        self.con = sqlite3.connect("WordsDB/words.db")
        self.setupUi()
        self.setupBackEnd()

    def setupUi(self):
        # ------------------------------------Курсы-------------------------------------
        self.title = QLabel(self)
        self.title.setText("Курсы")
        self.title.setFont(QFont("Yu Gothic UI Semibold", 18))

        is_using = lambda name: int(
            1 in [
                i[0] for i in self.con.cursor()
                    .execute(f"SELECT is_using FROM {name}")
                    .fetchall()
            ]
        )
        self.englishCourse = CourseButton(
            self,
            "englishSlangCourse",
            is_using("englishSlangCourse"),
            "Английский",
            "сленг",
            "Выучи перевод и определения фраз",
        )
        self.russianCourse = CourseButton(
            self,
            "russianMedicineCourse",
            is_using("russianMedicineCourse"),
            "Русский",
            "медицинский",
            "Выучи определения слов",
        )
        self.spainCourse = CourseButton(
            self,
            "spainBaseCourse",
            is_using("spainBaseCourse"),
            "Испанский",
            "базовый",
            "Выучи определения слов",
        )
        self.myCourse = CourseButton(
            self, "myCourse", is_using("myCourse"), "Мой курс", "", ""
        )

        # -------------------------------Кнопка настроек--------------------------------
        self.settingsButton = QPushButton(self)
        self.settingsButton.setIcon(QIcon("Icons/settingsButton.png"))
        self.settingsButton.setToolTip("Настройки")
        self.settingsButton.setIconSize(QSize(35, 35))
        self.settingsButton.setStyleSheet(get_invisible_settingsButton_StyleSheet())
        self.settingsButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.settingsButton.is_courseButton = False

        # --------------------------------Список курсов---------------------------------
        self.coursesGLayout = QGridLayout()
        self.coursesGLayout.setGeometry(QRect(0, 0, 800, 150))

        self.coursesGLayout.addWidget(self.title, 0, 0)
        self.coursesGLayout.addWidget(self.englishCourse.courseButton, 1, 0)
        self.coursesGLayout.addWidget(self.russianCourse.courseButton, 1, 1)
        self.coursesGLayout.addWidget(self.spainCourse.courseButton, 2, 0)
        self.coursesGLayout.addWidget(self.myCourse.courseButton, 2, 1)

        # ----------------------------Глобальная компоновка-----------------------------
        self.globalLayout = QVBoxLayout()
        self.globalLayout.addLayout(self.coursesGLayout)
        self.verticalSpacer = QSpacerItem(
            20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding
        )
        self.globalLayout.addItem(self.verticalSpacer)
        self.globalLayout.addWidget(
            self.settingsButton, alignment=Qt.AlignRight
        )  # Кнопка настроек в правом нижнем углу

        self.centralWidget = QWidget()
        self.centralWidget.setLayout(self.globalLayout)
        self.setCentralWidget(self.centralWidget)

    def setupBackEnd(self):
        # ----------------------------Открытие окна настроек----------------------------
        self.settingsButton.clicked.connect(self.showSettingsWindow)

        # -----------------------------Выбор/удаление курса-----------------------------
        for item in self.findChildren(QPushButton):
            item.clicked.connect(self.clickOnCourseButton)

    def showSettingsWindow(self):
        self.settings = SettingsWindow()
        self.settings.move(  # Размещение окна настроек по центру главного окна
            self.x() + self.width() // 2 - self.settings.width() // 2,
            self.y() + self.height() // 2 - self.settings.height() // 2,
        )
        self.settings.show()

    def clickOnCourseButton(self):
        sender = self.sender()
        if not sender.is_courseButton:
            return

        # ----------------------------Изменение цвета рамки-----------------------------
        if not sender.is_using:
            sender.setStyleSheet(get_selected_courseButton_StyleSheet())
            sender.is_using = True
        else:
            sender.setStyleSheet(get_courseButton_StyleSheet())
            sender.is_using = False

        # --------------------------Модификация текущего курса--------------------------
        query = f"""
            UPDATE {sender.name}
            SET is_using = {1 if sender.is_using == True else 0}
        """

        self.con.cursor().execute(query).fetchall()
        self.con.commit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    my_app = MainWindow()
    my_app.show()
    sys.exit(app.exec_())
