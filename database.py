import sqlite3
import pandas as pd

DB = "todo.db"

def init(db_name = DB):
    with sqlite3.connect(db_name ) as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY, name TEXT, status TEXT, date TEXT, user TEXT, note TEXT
        )
        """)
    conn.close()


def add_tk(name, status, date, user, note,db_name = DB):
    with sqlite3.connect(db_name) as conn:
        conn.execute("INSERT INTO tasks (name, status, date, user, note) VALUES (?,?,?,?,?)", (name, status, str(date), user, note))
    conn.close()


def get_tk(db_name = DB):
    with sqlite3.connect(db_name ) as conn:
        kq = pd.read_sql('SELECT * FROM tasks', conn)
    conn.close()
    return kq

# bài 4:
def get_tk_id(tid,db_name = DB):
    with sqlite3.connect(db_name ) as conn:
        kq = conn.execute("SELECT * FROM tasks WHERE id=?", (tid,)).fetchone()
    conn.close()
    return kq

def upd_tk(tid, name, stat, dt, user, note,db_name = DB):
    with sqlite3.connect(db_name ) as conn:
        conn.execute("UPDATE tasks SET name=?, status=?, date=?, user=?, note=? WHERE id=?", (name, stat, str(dt), user, note, tid))
    conn.close()

def del_tk(tid,db_name = DB):
    with sqlite3.connect(db_name) as conn:
        conn.execute("DELETE FROM tasks WHERE id=?", (tid,))
    conn.close()