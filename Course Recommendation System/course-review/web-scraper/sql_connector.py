import mysql
from mysql import connector


class Conn:
    def __init__(self):
        try:
            self.conn = mysql.connector.connect(user='root', password='Ge0rgi@Tec#')
            self.cursor = self.conn.cursor(buffered=True)
        except Exception as e:
            print e

    def create_database(self, DB_NAME):
        try:
            self.cursor.execute("CREATE DATABASE {}".format(DB_NAME))
            self.cursor.execute("USE {}".format(DB_NAME))
        except Exception as e:
            print e

    def create_table(self, TABLE_NAME):
        table_review = "CREATE TABLE {} (course_name TEXT, author_id TEXT, review_text TEXT, " \
                       "difficulty char(15), rating char(20), workload char(20))".format(TABLE_NAME)
        try:
            self.cursor.execute(table_review)
        except Exception as e:
            print e

    def insert_into_table(self, TABLE_NAME, values):
        insert_sql = "INSERT INTO {} (course_name, author_id, review_text, difficulty, rating, workload) " \
                     "VALUES (%s, %s, %s, %s, %s, %s)".format(TABLE_NAME)
        try:
            self.cursor.execute(insert_sql, values)
        except Exception as e:
            print e

    def duplicateSQL(self, TABLE_NAME):
        select_sql = "SELECT * FROM {}".format(TABLE_NAME)
        self.cursor.execute(select_sql)
        records = self.cursor.fetchone()
        print records

    def close_conn(self):
        self.conn.commit()
        self.cursor.close()
        self.conn.close
