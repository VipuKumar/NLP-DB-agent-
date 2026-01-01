from fastapi import APIRouter,HTTPException
from pydantic import BaseModel
import sqlite3


from hitl.write_set import compute_write_set
from audit.audit import write_audit_log

router=APIRouter()


class ExecuteRequest(BaseModel):
    sql:str
    write_set_hash:str
    approved_by:str



@router.post("/execute")


def execute(req:ExecuteRequest):
    conn=sqlite3.connect("db/example.db")

    cursor=conn.cursor()


    if "WHERE" not in req.sql.upper():
        raise HTTPException(status_code=400,detail="Unsafe execution request")
    

    where_clause=req.sql.split("WHERE",1)[1]

    ws=compute_write_set(conn,"users",where_clause)

    if ws["write_set_hash"]!=req.write_set_hash:
        raise HTTPException(
            status_code=409,
            detail="Database changed.Re-approval required"
        )
    

    try:
        cursor.execute("BEGIN IMMEDIATE;")
        cursor.execute(req.sql)


        write_audit_log(
            conn=conn,
            sql=req.sql,
            write_set_hash=req.write_set_hash,
            row_count=ws["row_count"],
            approved_by=req.approved_by

        )
        conn.commit()

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500,detail=str(e))
    

    finally:
        conn.close()



    return{
            "status":"executed",
            "rows_affected":ws["row_count"],
            "approved_by":req.approved_by



    }