from PyQt5.QtGui import QCursor, QFont, QIcon
from PyQt5.QtCore import QSettings, Qt
from PyQt5.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QSizePolicy,
    QSpacerItem,
    QWidget,
    QLabel,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QGroupBox
)
from style import get_saveButton_StyleSheet
import sys


class SettingsWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Настройки")
        self.setWindowIcon(QIcon("Icons/settingsAppIcon.png"))
        self.setGeometry(1000, 300, 300, 500)
        self.setupUi()
        self.setupBackEnd()

    def setupUi(self):
        # -------------------------Название раздела «Настройки»-------------------------
        self.title = QLabel(self)
        self.title.setText("Настройки")
        self.title.setFont(QFont("Yu Gothic UI Semibold", 18))

        # --------------------Настройка частоты отправки уведомлений--------------------
        self.delay = QGroupBox("Частота отправки уведомлений (час)", self)
        self.delay.setFont(QFont("Yu Gothic UI Semibold", 9))
        self.delay.setAlignment(Qt.AlignLeft)

        self.delaySB = QSpinBox(self.delay) 
        self.delaySB.setSingleStep(1)
        self.delaySB.setMinimum(1)
        self.delaySB.setMaximum(24)
        self.delaySB.setWrapping(True)
        self.delaySB.setSuffix(" h")

        self.hlayoutDelay = QHBoxLayout()
        self.hlayoutDelay.addWidget(self.delaySB)

        self.delay.setLayout(self.hlayoutDelay)

        # ------------------------------Кнопка «Сохранить»------------------------------
        self.saveButton = QPushButton(self)
        self.saveButton.setText("Сохранить")
        self.saveButton.setFont(QFont("Yu Gothic UI Semibold", 12))
        self.saveButton.setStyleSheet(get_saveButton_StyleSheet())
        self.saveButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.saveButton.hide()

        # ----------------------------Глобальная компоновка-----------------------------
        self.globalLayout = QVBoxLayout()
        self.globalLayout.addWidget(self.title)
        self.globalLayout.addWidget(self.delay)

        self.verticalSpacer = QSpacerItem(
            20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding
        )
        self.globalLayout.addItem(self.verticalSpacer)
        self.globalLayout.addWidget(self.saveButton, alignment=Qt.AlignRight)

        self.setLayout(self.globalLayout)
    
    def setupBackEnd(self):
        # ------------------------Установка значения в спинбокс-------------------------
        self.settings = QSettings('App/config.ini', QSettings.IniFormat)
        self.delaySB.setValue(self.settings.value('notificationDelay', 1, type=int))

        #------------------------------Сохранение настроек------------------------------
        self.delaySB.valueChanged.connect(lambda: self.saveButton.show())
        self.saveButton.clicked.connect(self.saveSettings)
    
    def saveSettings(self):
        self.settings.setValue('notificationDelay', self.delaySB.value())
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    my_app = SettingsWindow()
    my_app.show()
    sys.exit(app.exec_())
