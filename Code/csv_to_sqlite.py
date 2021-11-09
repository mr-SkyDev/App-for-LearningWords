import csv
import sqlite3


def main():
    filename = "spainBaseCourse"
    with open('WordsDB/' + filename + '.csv', encoding="utf-8") as csvfile:
        reader = csv.DictReader(
            csvfile, fieldnames=["word", "value"], quotechar='"', delimiter=";"
        )
        reader = list(reader)

        con = sqlite3.connect('WordsDB/words.db')
        for line in reader:
            cur = con.cursor()
            word, value = line['word'], line['value']

            query = f"""
                INSERT INTO {filename} (word, value, is_using)
                VALUES ("{word}", "{value}", 1)
            """
            cur.execute(query)
            con.commit()


if __name__ == "__main__":
    main()
