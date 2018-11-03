import mysql
from mysql import connector


class Conn:
    def __init__(self):
        try:
            self.conn = mysql.connector.connect(user='root', password='Ge0rgi@Tec#')
            self.cursor = self.conn.cursor()
        except Exception as e:
            print e

    def create_database(self, DB_NAME):
        try:
            self.cursor.execute("CREATE DATABASE {}".format(DB_NAME))
            self.cursor.execute("USE {}".format("COURSE_REVIEWS"))
        except Exception as e:
            print e

    def create_table(self, TABLE_NAME):
        table_review = "CREATE TABLE {} (course_name varchar(60), author_id char(30), review_text TEXT, " \
                       "difficulty char(10), liked char(10), workload char(20))".format(TABLE_NAME)
        try:
            self.cursor.execute(table_review)
        except Exception as e:
            print e

    def insert_into_table(self, TABLE_NAME, values):
        insert_sql = "INSERT INTO {} (course_name, author_id, review_text, difficulty, liked, workload) " \
                     "VALUES (%s, %s, %s, %s, %s, %s)".format(TABLE_NAME)
        try:
            self.cursor.execute(insert_sql, values)
        except Exception as e:
            print e


    def close_conn(self):
        self.cursor.close()
        self.conn.close
