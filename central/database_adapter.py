import sqlite3


class DatabaseAdapter:
    def __init__(self):
        self.DATABASE_FILE = "database.db"
        self.TABLE_NAME = "MEASUREMENTS"

        self.__init_table()

    def __init_table(self):
        sql = f"""
            CREATE TABLE IF NOT EXISTS "{self.TABLE_NAME}" (
                "SOURCE"	TEXT,
                "VALUE"	REAL,
                "TIME"	TEXT
            );
            """
        self.__execute_sql_query(sql)

    def __create_connection(self):
        conn = None
        try:
            conn = sqlite3.connect(self.DATABASE_FILE)
        except Error as e:
            print(e)
            raise e
        return conn

    def __execute_sql_query(self, query):

        with self.__create_connection() as conn:
            cur = conn.cursor()
            cur.execute(query)
            conn.commit()
            return cur.lastrowid

    def save_measurement(self, source, value, time):
        query = f"""\
INSERT INTO {self.TABLE_NAME}
VALUES ("{source}", {value}, {time})
"""
        print(query)
        return self.__execute_sql_query(query)
