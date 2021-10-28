import csv
from pprint import pprint
from os.path import exists  # Для проверки на существование файла/папки
from string import ascii_letters


clear_file = "WordsDB/en-rus-sleng.csv"  # Будущее название отчищенного файла
raw_file = "WordsDB/raw-en-rus-sleng.csv"  # Название сырого файла

if exists(clear_file):
    if (
        input(
            f'Чистый файл с названием "{clear_file}" уже существует. Вы хотите продолжить? +/- '
        )
        == "-"
    ):
        quit()
if not exists(raw_file):
    print(f'Файл "{raw_file}" не был найден')

with open(raw_file, encoding="utf-8") as f:
    reader = csv.DictReader(
        f, fieldnames=["word", "value"], delimiter=";", quotechar='"'
    )
    reader = list(reader)

with open(clear_file, "w", encoding="utf-8") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=["word", "value"],
        delimiter=";",
        quotechar='"',
        lineterminator="\n",
    )

    for line in reader:
        clear_word = line["word"].capitalize()
        clear_value = list(
            line["value"].replace('""', "")
        )  # Избавляемся от лишних ковычек

        # Очистка от слов в скобках
        while "(" in clear_value and ")" in clear_value:
            open_br = clear_value.index("(")
            close_br = clear_value.index(")")
            del clear_value[open_br : close_br + 1]

        # Очистка от английских букв в русском определении
        en_letters = filter(lambda x: x in ascii_letters, clear_value)

        clear_value = "".join(clear_value)
        for letter in en_letters:
            clear_value = clear_value.replace(letter, "")

        clear_value = clear_value.strip()

        # Нужно еще очистить лишние пробелы в значениях, там же лишние слова (после перевода примера)

        writer.writerow({"word": clear_word, "value": clear_value})
