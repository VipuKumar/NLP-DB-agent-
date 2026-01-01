import sqlite3
import hashlib

from typing import List,Tuple



class WriteSetError(Exception):
    pass

def _serialize(table:str,rows:List[Tuple[int,int]])->str:
    parts=[table]

    for rid,version in rows:
        parts.append(f"{rid}:{version}")
    return "|".join(parts)


def _hash(data:str)->str:
    return hashlib.sha256(data.encode()).hexdigest()



def compute_write_set(conn:sqlite3.Connection,table:str,where_clause:str)->dict:
    sql=f"""
    SELECT id,row_version
    FROM {table}
WHERE {where_clause}
                 """
    
    cursor=conn.cursor()
    cursor.execute(sql)
    rows=cursor.fetchall()


    if not rows:
        raise WriteSetError("Write-set is empty")
    

    rows.sort(key=lambda x:x[0])

    serialized=_serialize(table,rows)
    write_set_hash=_hash(serialized)


    return{
        "row_count":len(rows),
        "write_set_hash":write_set_hash



    }
