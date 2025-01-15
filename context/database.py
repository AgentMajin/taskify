import sqlite3
import os

db_context: sqlite3.Connection = None

currnet_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.abspath(os.path.join(currnet_dir, '..'))
db_path = os.path.join(project_dir, 'main_todo.db')

def connect_db() -> sqlite3.Connection:
    global db_context
    if(db_context is None):
        db_context = sqlite3.connect(db_path)
        print("Connected to db")
    return db_context

    # cursor = connect_db().cursor()
    # cursor.execute('SELECT * FROM Tasks')

    # for row in cursor.fetchall():
    #     print(row)

    # db_context.close()