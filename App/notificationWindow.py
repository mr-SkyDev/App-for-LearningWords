from PyQt5.QtCore import QEasingCurve, QPoint, QPropertyAnimation, Qt
from PyQt5.QtGui import QCursor, QFont, QIcon
from PyQt5.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QSizePolicy,
    QSpacerItem,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QApplication,
)

import ctypes
from style import (
    get_darkblue_notificationWindow_StyleSheet,
    get_notificationButton_StyleSheet,
)


# Получение размера дисплея (у некоторых может быть другой размер)
user32 = ctypes.windll.user32

user32.SetProcessDPIAware()
DISPAYWIDTH, DISPLAYHEIGHT = (user32.GetSystemMetrics(0), user32.GetSystemMetrics(1))


class NotificationWindow(QWidget):
    def __init__(self, word, value, title="App for LearningWords"):
        super().__init__()

        self.showFullButton = False
        self.word = word
        self.rawValue = value
        self.value = value
        self.title = title

        self.lines = len(word + value) // 54 + 1
        if self.lines > 10:
            self.lines = 10
            self.value = self.value[:54 * 6 - 3] + "..."
            self.showFullButton = True

        self.setupUi()
        self.setupBackEnd()

    def setupUi(self):
        self.setWindowTitle(self.title)
        self.setFixedSize(400, 150 + 18 * self.lines)
        self.move(QPoint(DISPAYWIDTH + 5, DISPLAYHEIGHT - self.height() - 80))
        self.setWindowIcon(QIcon("Icons/AppIcon_v3.png"))
        self.setStyleSheet(get_darkblue_notificationWindow_StyleSheet())

        # ----------------------------Содержимое уведомления----------------------------
        self.wordLbl = QLabel(self)
        self.wordLbl.setWordWrap(True)
        self.wordLbl.setText(self.word)
        self.wordLbl.setFont(QFont("Yu Gothic UI Semibold", 10))
        self.wordLbl.setTextInteractionFlags(Qt.TextSelectableByMouse)

        # Горизонтальная линия
        self.hLine = QLabel(self)
        self.hLine.setFixedHeight(2)
        self.hLine.setStyleSheet("""background-color: #000000""")

        self.valueLbl = QLabel(self)
        self.valueLbl.setWordWrap(True)
        self.valueLbl.setText(self.value)
        self.valueLbl.setFont(QFont("Yu Gothic UI Semibold", 9))
        self.valueLbl.setTextInteractionFlags(Qt.TextSelectableByMouse)

        self.wordValueLayout = QVBoxLayout()
        self.wordValueLayout.addWidget(self.wordLbl)
        self.wordValueLayout.addWidget(self.hLine)
        self.wordValueLayout.addWidget(self.valueLbl)

        # Кнопки
        if self.showFullButton:
            self.fullButton = QPushButton(self)
            self.fullButton.setText("Показать полностью")
            self.fullButton.setStyleSheet(get_notificationButton_StyleSheet())
            self.fullButton.setCursor(QCursor(Qt.PointingHandCursor))
            self.fullButton.clicked.connect(self.showFullNotificationWindow)
            self.fullButton.setFont(QFont("Yu Gothic UI Semibold", 9))
            self.wordValueLayout.addWidget(self.fullButton)

        self.okButton = QPushButton(self)
        self.okButton.setText("Понял")
        self.okButton.setStyleSheet(get_notificationButton_StyleSheet())
        self.okButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.okButton.setFont(QFont("Yu Gothic UI Semibold", 9))

        self.learnButton = QPushButton(self)
        self.learnButton.setText("Выучил")
        self.learnButton.setStyleSheet(get_notificationButton_StyleSheet())
        self.learnButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.learnButton.setFont(QFont("Yu Gothic UI Semibold", 9))

        self.horizontalSpacer = QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum
        )

        self.buttonsLayout = QHBoxLayout()
        self.buttonsLayout.addWidget(self.okButton)
        self.buttonsLayout.addWidget(self.learnButton)
        self.buttonsLayout.addItem(self.horizontalSpacer)

        # Глобальная компоновка
        self.globalLayout = QVBoxLayout()

        self.verticalSpacer = QSpacerItem(
            20, 70, QSizePolicy.Minimum, QSizePolicy.Expanding
        )

        self.globalLayout.addLayout(self.wordValueLayout)
        self.globalLayout.addItem(self.verticalSpacer)
        self.globalLayout.addLayout(self.buttonsLayout)
        self.setLayout(self.globalLayout)

    def setupBackEnd(self):
        self.okButton.clicked.connect(self.closeEvent)
        self.learnButton.clicked.connect(self.closeEvent)

        # ----------------------------Анимация появления окна---------------------------
        self.selfAnimationPos = QPropertyAnimation(self, b"pos")
        self.selfAnimationPos.setDuration(300)

        self.doPosAnimation()

    def showFullNotificationWindow(self):
        self.fullNotificationWindow = FullNotificationWindow(
            self.title, self.word, self.rawValue
        )
        self.fullNotificationWindow.exec()

    def doPosAnimation(self):
        self.selfAnimationPos.stop()

        self.selfAnimationPos.setStartValue(
            # QPoint(DISPAYWIDTH + 5, DISPLAYHEIGHT - self.height() - 80)
            QPoint(self.x(), self.y())
        )
        self.selfAnimationPos.setEasingCurve(QEasingCurve.OutBack)  #InOutCubic

        self.selfAnimationPos.setEndValue(
            QPoint(DISPAYWIDTH - self.width() - 5, DISPLAYHEIGHT - self.height() - 80)
        )

        self.selfAnimationPos.start()

    def closeEvent(self, event):
        self.selfAnimationPos.stop()
        self.selfAnimationPos.finished.connect(self.close)

        self.selfAnimationPos.setStartValue(
            # QPoint(DISPAYWIDTH - self.width() - 5, DISPLAYHEIGHT - self.height() - 80)
            QPoint(self.x(), self.y())
        )
        self.selfAnimationPos.setEasingCurve(QEasingCurve.InBack)
        self.selfAnimationPos.setEndValue(
            QPoint(DISPAYWIDTH + 5, DISPLAYHEIGHT - self.height() - 80)  # 80 - 
            #                                              высота таскбара (os: windows)
        )

        self.selfAnimationPos.start()


class FullNotificationWindow(QDialog):
    def __init__(self, title, word, value):
        super().__init__()

        self.title = title
        self.word = word
        self.value = value

        self.setupUi()

    def setupUi(self):
        self.setWindowTitle(self.title)
        self.setMinimumWidth(300)
        self.move(DISPAYWIDTH - 500, DISPLAYHEIGHT - 500)
        self.setWindowIcon(QIcon("Icons/AppIcon_v3.png"))
        self.setStyleSheet(get_darkblue_notificationWindow_StyleSheet())

        self.wordLbl = QLabel(self)
        self.wordLbl.setWordWrap(True)
        self.wordLbl.setText(self.word)
        self.wordLbl.setFont(QFont("Yu Gothic UI Semibold", 10))
        self.wordLbl.setTextInteractionFlags(Qt.TextSelectableByMouse)

        self.hLine = QLabel(self)
        self.hLine.setFixedHeight(2)
        self.hLine.setStyleSheet("""background-color: #000000""")

        self.valueLbl = QLabel(self)
        self.valueLbl.setWordWrap(True)
        self.valueLbl.setText(self.value)
        self.valueLbl.setFont(QFont("Yu Gothic UI Semibold", 9))
        self.valueLbl.setTextInteractionFlags(Qt.TextSelectableByMouse)

        self.wordValueLayout = QVBoxLayout()
        self.wordValueLayout.addWidget(self.wordLbl)
        self.wordValueLayout.addWidget(self.hLine)
        self.wordValueLayout.addWidget(self.valueLbl)
        self.wordValueLayout.addItem(
            QSpacerItem(20, 70, QSizePolicy.Minimum, QSizePolicy.Expanding)
        )

        self.setLayout(self.wordValueLayout)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    title = "englishSlang"
    word = "ODD BALL"
    value = (
        'n. informal эксцентричная личность, ""белая ворона"", ""сумасшедший'
        ' заяц"", ненормальный: Please don`t deal with him. He is an odd ball.-Лучше'
        " не связывайся ты с ним. Он с головой не дружит."
    )
    w = NotificationWindow(word, value, title)
    w.show()
    sys.exit(app.exec_())
