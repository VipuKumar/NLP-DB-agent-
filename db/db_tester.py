import sqlite3
database_file="example.db"

def init_db():
    conn=sqlite3.connect(database_file)
    cursor=conn.cursor()
    cursor.execute("""
        SELECT * FROM audit_log"""
    )
    rows=cursor.fetchall()
    conn.close()
    print("Current entries in the users table:")
    for row in rows:
        print(row)  

init_db()