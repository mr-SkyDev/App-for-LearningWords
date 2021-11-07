from PyQt5.QtCore import QEasingCurve, QPoint, QPropertyAnimation, Qt
from PyQt5.QtGui import QCursor, QFont
from PyQt5.QtWidgets import (
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


# Получение размера дисплея (у некоторых другой)
user32 = ctypes.windll.user32

user32.SetProcessDPIAware()
DISPAYWIDTH, DISPLAYHEIGHT = (user32.GetSystemMetrics(0), user32.GetSystemMetrics(1))


class NotificationWindow(QWidget):
    def __init__(self, title, word, value):
        super().__init__()
        self.word = word
        self.value = value
        self.title = title

        self.setupUi()
        self.setupBackEnd()

    def setupUi(self):
        self.setWindowTitle(self.title)
        self.setFixedSize(400, 200)
        self.setStyleSheet(get_darkblue_notificationWindow_StyleSheet())

        # ----------------------------Содержимое уведомления----------------------------
        self.wordLbl = QLabel(self)
        self.wordLbl.setText(self.word)
        self.wordLbl.setFont(QFont("Yu Gothic UI Semibold", 10))

        # Горизонтальная линия
        self.hLine = QLabel(self)
        self.hLine.setFixedHeight(2)
        self.hLine.setStyleSheet("""background-color: #000000""")

        self.valueLbl = QLabel(self)
        self.valueLbl.setText(self.value)
        self.valueLbl.setFont(QFont("Yu Gothic UI Semibold", 10))

        self.wordValueLayout = QVBoxLayout()
        self.wordValueLayout.addWidget(self.wordLbl)
        self.wordValueLayout.addWidget(self.hLine)
        self.wordValueLayout.addWidget(self.valueLbl)

        # Кнопки
        self.okButton = QPushButton(self)
        self.okButton.setText("Понял")
        self.okButton.setStyleSheet(get_notificationButton_StyleSheet())
        self.okButton.setCursor(QCursor(Qt.PointingHandCursor))

        self.learnButton = QPushButton(self)
        self.learnButton.setText("Выучил")
        self.learnButton.setStyleSheet(get_notificationButton_StyleSheet())
        self.learnButton.setCursor(QCursor(Qt.PointingHandCursor))

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
        self.okButton.clicked.connect(self.closeWindowPosAnimation)

        # ----------------------------Анимация появления окна---------------------------
        self.selfAnimationPos = QPropertyAnimation(self, b"pos")
        self.selfAnimationPos.setDuration(200)

        self.doPosAnimation()

    def doPosAnimation(self):
        self.selfAnimationPos.stop()

        self.selfAnimationPos.setStartValue(
            QPoint(DISPAYWIDTH, DISPLAYHEIGHT - self.height() - 80)
        )
        self.selfAnimationPos.setEasingCurve(QEasingCurve.InOutCubic)

        self.selfAnimationPos.setEndValue(
            QPoint(DISPAYWIDTH - self.width() - 5, DISPLAYHEIGHT - self.height() - 80)
        )

        self.selfAnimationPos.start()

    def closeWindowPosAnimation(self):
        self.selfAnimationPos.stop()
        self.selfAnimationPos.finished.connect(self.close)

        self.selfAnimationPos.setStartValue(
            QPoint(DISPAYWIDTH - self.width() - 5, DISPLAYHEIGHT - self.height() - 80)
        )
        self.selfAnimationPos.setEasingCurve(QEasingCurve.InOutCubic)
        self.selfAnimationPos.setEndValue(
            QPoint(DISPAYWIDTH - 5, DISPLAYHEIGHT - self.height() - 80)
        )

        self.selfAnimationPos.start()


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    w = NotificationWindow("englishSlang", "nigga", "негр")
    w.show()
    sys.exit(app.exec_())
