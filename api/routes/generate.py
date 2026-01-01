from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import sqlite3

from agents.read_agent import ReadAgent
from agents.write_agent import WriteAgent

from validation.ast_validator import validate_ast
from validation.rule_validator import validate_rules, RuleViolation
from hitl.write_set import compute_write_set
from execution.sqlite_executor import execute_select
from execution.sql_rewriter import enforce_update_invariants

router = APIRouter()


class GenerateRequest(BaseModel):
    question: str
    mode: str


@router.post("/generate")
def generate(req: GenerateRequest):
    schema = """
    users(
        id INTEGER,
        name TEXT,
        age INTEGER,
        email TEXT,
        active INTEGER,
        role TEXT,
        row_version INTEGER,
        created_at TEXT,
        updated_at TEXT
    )
    """

    # -------- GENERATE --------
    if req.mode == "read":
        sql = ReadAgent().generate_sql(req.question, schema)

    elif req.mode == "write":
        out = WriteAgent().generate_sql(req.question, schema)

        if out["type"] == "error":
            raise HTTPException(status_code=400, detail=out["message"])

        sql = out["query"]

        # ✅ correct place for invariant enforcement
        sql = enforce_update_invariants(sql)
        print(sql)

    else:
        raise HTTPException(status_code=400, detail="Invalid mode")

    # -------- VALIDATE --------
    try:
        validate_ast(
            sql,
            allowed_tables={"users"},
            allowed_columns={
                "users": {"id", "name", "age", "email", "active", "role", "row_version","created_at","updated_at"}
            }
        )
        validate_rules(sql)

    except RuleViolation as e:
        raise HTTPException(status_code=400, detail=str(e))

    # -------- READ --------
    if req.mode == "read":
        rows = execute_select("db/example.db", sql)
        return {
            "sql": sql,
            "rows": rows
        }

    # -------- WRITE --------
    response = {"sql": sql}

    conn = sqlite3.connect("db/example.db")
    try:
        if "WHERE" not in sql.upper():
            raise HTTPException(status_code=400, detail="Write query must have WHERE")

        where_clause = sql.split("WHERE", 1)[1]
        ws = compute_write_set(conn, "users", where_clause)

        response.update({
            "row_count": ws["row_count"],
            "write_set_hash": ws["write_set_hash"]
        })

    finally:
        conn.close()

    return response
