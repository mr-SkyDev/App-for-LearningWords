def get_courseButton_StyleSheet():
    """ Кнопка курса """ 

    return """
        QPushButton {
            border: none;
            background-color: #DCDCDC;
            border-radius: 10px;
            border: 2px solid #000000;
        }

        /* Наведение на кнопку */
        QPushButton:hover {
            background-color: #D3D3D3;
        }

        /* Нажатие на кнопку */
        QPushButton:pressed {
            background-color: #C0C0C0;
            border: 2px solid #696969;
        }
    """


def get_courseButton_titleLabel_StyleSheet():
    """ Текст на кнопке курса: название курса """

    return """
        QLabel {
            font-size: 16px;
        }
    """


def get_courseButton_complexityLabel_StyleSheet():
    """ Текст на кнопке курса: сложность курса """

    return """
        #CourseButton-ComplexityLabel {
            color: #696969;
            font-size: 13px;
            font-style: italic;
        }
    """


def get_courseButton_descriptionLabel_StyleSheet():
    """ Текст на кнопке курса: описание курса """

    return """
        #CourseButton-DescriptionLabel {
            font-size: 14px;
        }
    """


def get_invisible_settingsButton_StyleSheet():
    """ Прозрачная кнопка настроек """

    return """
        QPushButton {
            background-color: rgba(255, 255, 255, 0);
        }

        QPushButton:hover {
            border-radius: 22px;
            background-color: rgba(100, 100, 100, 40);
        }

        QPushButton:pressed {
            background-color: rgba(0, 0, 0, 70);
        }
    """


def get_saveButton_StyleSheet():
    """ Кнопка «Сохранить» """

    return """
        QPushButton {
            border: 2px solid #000000;
            border-radius: 6px;
            padding: 2px 5px;
        }

        QPushButton:hover {
            background-color: #DCDCDC;
        }

        QPushButton:pressed {
            background-color: #C0C0C0;
            border: 2px solid #696969;
        }
    """


def get_selected_courseButton_StyleSheet():
    """ Выбранный курс """

    return """
        QPushButton {
            border: 5px solid #FF4040;
            background-color: #DCDCDC;
            border-radius: 10px;
        }

        QPushButton:hover {
            background-color: #D3D3D3;
        }

        QPushButton:pressed {
            background-color: #C0C0C0;
            border: 5px solid #D5713F;
        }
    """

def get_changeViewButton_StyleSheet():
    """ Изменить отображение таблицы """

    return """
        QPushButton {
            border: 2px solid #000000;
            border-radius: 6px;
            padding: 2px 5px;
        }

        QPushButton:hover {
            background-color: #DCDCDC;
        }

        QPushButton:pressed {
            background-color: #C0C0C0;
            border: 2px solid #696969;
        }
    """


def get_addRowButton_StyleSheet():
    """ Добавить строку в таблицу """

    return """
        QPushButton {
            border: 2px solid #000000;
            border-radius: 6px;
            padding: 2px 5px;
        }

        QPushButton:hover {
            background-color: #DCDCDC;
        }

        QPushButton:pressed {
            background-color: #C0C0C0;
            border: 2px solid #696969;
        }
    """

def get_nonclickeble_saveButton_StyleSheet():
    """ Некликабельная кнопка сохранения """
    
    return """
        QPushButton {
            /*background-color: #828282;*/
            padding: 2px 5px;
            color: #464451;
            border-radius: 6px;
            border: 2px solid #606E8C;
        }
    """


def get_darkblue_notificationWindow_StyleSheet():
    """ Темно синяя тема для окна уведомлений """

    return """
        QWidget {
            background-color: #0000ff;
        }
    """


def get_notificationButton_StyleSheet():
    """ Кнопка «понял» для окна уведомлений """

    return """
        QPushButton {
            border: none;
            background-color: 0000ff;
            border-radius: 5px;
            border: 2px solid #000000;
            padding: 3px 30px 3px 30px
        }

        QPushButton:hover {
            background-color: #42AAFF;
        }

        QPushButton:pressed {
            background-color: #0000C8;
            border: 2px solid #000000;
        }
    """