import sqlite3 as lite

class Db:
    """docstring for Db. """

    def __init__(self):
        self.db = '../../db/cycling.db'

    def insert(self, elem):
        print(elem)
        con = lite.connect(self.db) 

        for key, value in elem.__dict__:
            print(key, value)

        con.execute('''
            INSERT INTO
        ''')

        con.close()
