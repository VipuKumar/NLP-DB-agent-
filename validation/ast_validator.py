import sqlglot
from sqlglot import exp 


class ASTValidationError(Exception):
    pass


ALLOWED_STATEMENTS={
     exp.Select,
     exp.Insert,
     exp.Update,
     exp.Delete,
}


def validate_sql(sql:str,allowed_tables:set,allowed_columns:dict)->None:
    try:
        tree=sqlglot.parse_one(sql)
    except Exception as e:
        raise ASTValidationError("SQL parse erroe: {e}")
    


    if type(tree) not in ALLOWED_STATEMENTS:
      raise ASTValidationError("SQL statement type not allowed")



    tables={t.name for t in tree.find_all(exp.Table)}
    for table in tables:
        if table not in allowed_tables:
            raise ASTValidationError(f"Access to table '{table} is not allowed'")



    for col in tree.find_all(exp.Column):
        table=col.table
        column=col.name


        if table and table not in allowed_columns:
            raise ASTValidationError(f"Unknown table {table}")


        if table and column not in allowed_columns[table]:
            raise ASTValidationError(
                f"Unknown column {column} in table {table}"
            )                          

