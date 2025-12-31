import re



class RuleViolation(Exception):
    pass


BLACKLIST = {"DROP", "ALTER", "TRUNCATE"}
TAUTOLOGIES = [
    r"WHERE\s+1\s*=\s*1",
    r"WHERE\s+TRUE",
    r"WHERE\s+FALSE\s*=\s*FALSE",
    r"WHERE\s+\w+\s*=\s*\w+",
]


def validate_rules(sql:str)->None:
    sql_upper=sql.upper().strip()


    if ";" in sql_upper[:-1]:
        raise RuleViolation("Multiple Sql queries not allowed")


    for cmd in BLACKLIST:
        if cmd in sql_upper:
            raise RuleViolation(f"Forbidden command detected: {cmd}")
        



    if sql_upper.startswith(("UPDATE","DELETE")):
        if "WHERE" not in sql_upper:
            raise RuleViolation("UPDATE/DELETE without WHERE is not allowed")
        

        for patter in TAUTOLOGIES:
            if re.search(patter,sql_upper):
                raise RuleViolation("Tautological WHERE clause detected")
        


            

