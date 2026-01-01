import sqlite3
from typing import List,Tuple

def execute_select(db_path:str,sql:str)->List[Tuple]:
    conn=sqlite3.connect(db_path)
    cursor=conn.cursor()


    try:
        cursor.execute(sql)
        rows=cursor.fetchall()
        return rows
    finally:
        conn.close()