import sqlite3
import time
from datetime import datetime
import random
import matplotlib.pyplot as plt
from matplotlib import style
style.use('fivethirtyeight')

class Data:
    def __init__(self):
        self.conn=sqlite3.connect("data.db")
        self.c=self.conn.cursor()
        self.c.execute("CREATE TABLE IF NOT EXISTS users(unix REAL, datestamp TEXT, username TEXT, password TEXT)")

    def create_table(self, name):
        query="CREATE TABLE IF NOT EXISTS {}(unix REAL, datestamp TEXT, username TEXT, password TEXT, key TEXT)".format(name)
        self.c.execute(query)

    def get_all_tables(self):
        output=[]
        self.c.execute("SELECT name from sqlite_master WHERE type='table'")
        for i in self.c.fetchall():
            output.append(''.join(i))
        return output

    def check_table(self, name, username, password):
        self.c.execute("SELECT * FROM {}".format(name))
        for row in self.c.fetchall():
            if row[2]==username and row[3]==password:
                return True
        return False

    def read_table(self, name):
        self.c.execute("SELECT * FROM {}".format(name))
        for row in self.c.fetchall():
            print(row)

    def user_entry(self, username, password):
        unix_time=time.time()
        date=datetime.fromtimestamp(unix_time).strftime('%Y-%m-%d %H:%M:%S')
        self.c.execute("INSERT INTO users (unix, datestamp, username, password) VALUES (?, ?, ?, ?)",(unix_time, date, username, password))
        self.conn.commit()

    def group_entry(self, group_name, username, password, key):
        unix_time=time.time()
        date=datetime.fromtimestamp(unix_time).strftime('%Y-%m-%d %H:%M:%S')
        self.c.execute("INSERT INTO {} (unix, datestamp, username, password, key) VALUES (?, ?, ?, ?, ?)".format(group_name),(unix_time, date, username, password, key))
        self.conn.commit()

if __name__=="__main__":
    obj=Data()
    tables=obj.get_all_tables()
    for i in tables:
        obj.read_table(i)