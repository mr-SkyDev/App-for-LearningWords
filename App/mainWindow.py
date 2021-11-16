import sqlite3

from PyQt5 import QtGui
from PyQt5.QtGui import QCursor, QFont, QIcon
from PyQt5.QtCore import QRect, QSettings, QSize, QTimer, Qt
from PyQt5.QtWidgets import (
    QAction,
    QApplication,
    QLabel,
    QMainWindow,
    QMenu,
    QPushButton,
    QSizePolicy,
    QSystemTrayIcon,
    QWidget,
    QGridLayout,
    QVBoxLayout,
    QSpacerItem,
    qApp,
)

from style import *  # Стили для виджетов
from settingsWindow import SettingsWindow
from courseViewWindow import CourseViewWindow


class CourseButton(QPushButton):
    def __init__(
        self,
        parent,
        name,
        is_using,
        title="Курс",
        complexity="Сложность",
        description="Описание",
    ):
        super().__init__(parent)

        self.is_using = is_using
        self.is_courseButton = True
        self.name = name
        self.parent = parent

        # Кнопка курса
        # self.courseButton = QPushButton(parent)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setFixedSize(400, 150)
        self.setStyleSheet(
            get_courseButton_StyleSheet()
            if is_using == 0
            else get_selected_courseButton_StyleSheet()
        )

        # Название курса
        self.title = QLabel(
            title, self, objectName="CourseButton-TitleLabel"
        )
        self.title.move(10, 10)
        self.title.setStyleSheet(get_courseButton_titleLabel_StyleSheet())

        # Сложность курса
        self.complexity = QLabel(
            complexity, self, objectName="CourseButton-ComplexityLabel"
        )
        self.complexity.move(10, 27)
        self.complexity.setStyleSheet(get_courseButton_complexityLabel_StyleSheet())

        # Описание курса
        self.description = QLabel(
            description,
            self,
            objectName="CourseButton-DescriptionLabel",
        )
        self.description.move(10, 127)
        self.description.setStyleSheet(get_courseButton_descriptionLabel_StyleSheet())
    
    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        if event.button() == Qt.RightButton:
            self.courseView = CourseViewWindow(self, self.name)
            self.courseView.show()
        elif event.button() == Qt.LeftButton:
            self.parent.clickOnCourseButton(self)

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
        self.coursesGLayout.addWidget(self.englishCourse, 1, 0)
        self.coursesGLayout.addWidget(self.russianCourse, 1, 1)
        self.coursesGLayout.addWidget(self.spainCourse, 2, 0)
        self.coursesGLayout.addWidget(self.myCourse, 2, 1)

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
        # реализовано в методе clickOnCourseButton, который вызывается в методе кнопки 
        # курса mousePressEvent при нажатии на ЛКМ

        # --------------------------------Работа с треем--------------------------------
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon("Icons/appIcon_v3.png"))
 
        """
            Объявим и добавим действия для работы с иконкой системного трея
            show - показать окно
            hide - скрыть окно
            exit - выход из программы
        """
        self.show_action = QAction("Show", self)
        self.quit_action = QAction("Exit", self)
        self.hide_action = QAction("Hide", self)
        self.show_action.triggered.connect(self.show)
        self.hide_action.triggered.connect(self.hide)
        self.quit_action.triggered.connect(qApp.quit)
        self.tray_menu = QMenu()
        self.tray_menu.addAction(self.show_action)
        self.tray_menu.addAction(self.hide_action)
        self.tray_menu.addAction(self.quit_action)
        self.tray_icon.setContextMenu(self.tray_menu)
        self.tray_icon.show()

    def showSettingsWindow(self):
        self.settings = SettingsWindow()
        self.settings.move(  # Размещение окна настроек по центру главного окна
            self.x() + self.width() // 2 - self.settings.width() // 2,
            self.y() + self.height() // 2 - self.settings.height() // 2,
        )
        self.settings.show()

    def clickOnCourseButton(self, button):
        # ----------------------------Изменение цвета рамки-----------------------------
        if not button.is_using:
            button.setStyleSheet(get_selected_courseButton_StyleSheet())
            button.is_using = True
        else:
            button.setStyleSheet(get_courseButton_StyleSheet())
            button.is_using = False

        # --------------------------Модификация текущего курса--------------------------
        query = f"""
            UPDATE {button.name}
            SET is_using = {1 if button.is_using == True else 0}
        """

        self.con.cursor().execute(query).fetchall()
        self.con.commit()
    
    def closeEvent(self, event):
        event.ignore()  # Игнорируем отключение окна
        self.hide()  # Скрываем окно


# Получение списка таблиц-курсов
con = sqlite3.connect("WordsDB/words.db")
cur = con.cursor()
ignore_courses = ['sqlite_sequence']
courses = list(filter(lambda x: x not in ignore_courses, map(lambda x: x[0], 
    cur.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall())
))


def show_notification():
    from notificationWindow import NotificationWindow

    # Получение списка используемых слов и их значений
    words_values = list()
    for course in courses:
        cur = con.cursor()
        query = f"""
            SELECT word, value FROM {course}
            WHERE is_using = 1
        """
        res = cur.execute(query).fetchall()
        if res:
            words_values.append({course: res})

    # Если ни один курс не выбран, то ничего не делаем
    if not words_values:
        return

    def get_notification_value():
        current_word_value = choice(words_values)
        title = list(current_word_value.keys())[0]
        res = choice(current_word_value[title])
        return res[0], res[1], title

    notification = NotificationWindow(*get_notification_value())
    notification.show()


def notification_loop(parent):
    settings = QSettings("App/config.ini", QSettings.IniFormat)
    notification_delay = settings.value("notificationDelay", 1, type=int)

    # Каждый определенный час будет присылаться уведомление 
    tmr = QTimer(parent)
    tmr.timeout.connect(show_notification)
    tmr.start(notification_delay * 3_600_000)  # tmr.start(notification_delay * 1000)


if __name__ == "__main__":
    import sys
    from random import choice

    # Открытие приложения
    app = QApplication(sys.argv)
    my_app = MainWindow()
    my_app.show()

    # Старт цикла уведомлений
    notification_loop(my_app)

    # Завершение работы приложения
    sys.exit(app.exec_())
