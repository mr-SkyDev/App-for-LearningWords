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
from PyQt5.QtGui import QCursor, QIcon
from style import *  # Стили для виджетов
import sys


class CourseButton(QWidget):
    def __init__(self, parent='Курс', title='', complexity='', description=''):
        super().__init__()

        # Кнопка курса
        self.courseButton = QPushButton(parent)
        self.courseButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.courseButton.setFixedSize(400, 150)
        self.courseButton.setStyleSheet(get_courseButton_StyleSheet())

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


class Interface(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("App for LearningWords")
        self.setGeometry(300, 300, 700, 700)
        self.setupUi()

    def setupUi(self):
        self.englishCourse = CourseButton(
            self, "Английский", "сленг", "Выучи перевод и определения фраз"
        )
        self.russianCourse = CourseButton(
            self, "Русский", "медицинский", "Выучи определения слов"
        )
        self.spainCourse = CourseButton(
            self, "Испанский", "базовый", "Выучи определения слов"
        )
        self.myCourse = CourseButton(
            self, "Мой курс"
        )
        
        # Кнопка настроек
        self.settingsButton = QPushButton(self)
        self.settingsButton.setIcon(QIcon('Icons/settingsButton.png'))
        self.settingsButton.setToolTip('Настройки')
        self.settingsButton.setIconSize(QSize(35, 35))
        self.settingsButton.setStyleSheet(get_invisible_settingsButton_StyleSheet())
        self.settingsButton.setCursor(QCursor(Qt.PointingHandCursor))

        self.coursesGLayout = QGridLayout()
        self.coursesGLayout.setGeometry(QRect(0, 0, 800, 150))

        self.coursesGLayout.addWidget(self.englishCourse.courseButton, 0, 0)
        self.coursesGLayout.addWidget(self.russianCourse.courseButton, 1, 0)
        self.coursesGLayout.addWidget(self.spainCourse.courseButton, 0, 1)
        self.coursesGLayout.addWidget(self.myCourse.courseButton, 1, 1)

        # Глобальная компоновка
        self.globalLayout = QVBoxLayout()
        self.globalLayout.addLayout(self.coursesGLayout)
        self.verticalSpacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.globalLayout.addItem(self.verticalSpacer)
        self.globalLayout.addWidget(self.settingsButton, alignment=Qt.AlignRight)  # Кнопка настроек в правом нижнем углу

        self.centralWidget = QWidget()
        self.centralWidget.setLayout(self.globalLayout)
        self.setCentralWidget(self.centralWidget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    my_app = Interface()
    my_app.show()
    sys.exit(app.exec_())
