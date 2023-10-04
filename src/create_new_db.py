import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def main():
    database = r"dictionary_my.db"
    sql_create_dictionary_table = """ CREATE TABLE IF NOT EXISTS dictionary (
                                        id integer PRIMARY KEY,
                                        word text,
                                        meaning text
                                    ); """

    conn = create_connection(database)
    if conn is not None:
        create_table(conn, sql_create_dictionary_table)
    else:
        print("Ошибка: не удалось подключиться к базе.")


if __name__ == '__main__':
    main()
