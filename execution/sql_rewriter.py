from validation.rule_validator import RuleViolation

def enforce_update_invariants(sql: str) -> str:
    if not sql:
        return sql

    sql_clean = sql.strip()

    # normalize
    upper = sql_clean.upper()

    # only touch UPDATE
    if not upper.startswith("UPDATE"):
        return sql

    # already enforced
    if "ROW_VERSION" in upper and "UPDATED_AT" in upper:
        return sql

    if "WHERE" not in upper:
        raise RuleViolation("UPDATE must have WHERE clause")

    # split safely
    before_where, where_part = sql_clean.rsplit("WHERE", 1)

    if "SET" not in before_where.upper():
        raise RuleViolation("Invalid UPDATE syntax")

    # remove trailing semicolon if present
    before_where = before_where.rstrip().rstrip(";")
    where_part = where_part.strip().rstrip(";")

    rewritten = (
        f"{before_where}, "
        f"row_version = row_version+1, "
        f"updated_at = CURRENT_TIMESTAMP "
        f"WHERE {where_part};"
    )

    return rewritten
