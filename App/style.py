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
            border-radius: 10px;
            padding: 0px 5px;
        }

        QPushButton:hover {
            background-color: #DCDCDC;
        }

        QPushButton:pressed {
            background-color: #C0C0C0;
            border: 2px solid #696969;
        }
    """