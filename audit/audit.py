import hashlib
import sqlite3

def hash_sql(sql:str)->str:
    return hashlib.sha256(sql.encode()).hexdigest()





def write_audit_log(conn:sqlite3.Connection,sql:str,
                    write_set_hash:str,
                    row_count:int,
                    approved_by:str)->None:
    sql_hash=hash_sql(sql)

    conn.execute(
        """
    INSERT INTO audit_log(
        sql,
        sql_hash,
        write_set_hash,
        row_count,
        approved_by)VALUES(?,?,?,?,?)
""",
    (sql,sql_hash,write_set_hash,row_count,approved_by)
    )

    