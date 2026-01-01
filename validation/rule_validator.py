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
    print("VALIDATING:",sql)
    sql_upper=sql.upper().strip()



    for cmd in BLACKLIST:
        if cmd in sql_upper:
            raise RuleViolation(f"Forbidden command detected: {cmd}")
        



    if sql_upper.startswith(("UPDATE","DELETE")):
        if "WHERE" not in sql_upper:
            raise RuleViolation("UPDATE/DELETE without WHERE is not allowed")
        

    #if sql_upper.startswith("UPDATE"):
     #   if "ROW_VERSION=ROW_VERSION+1" not in sql_upper:
      #      raise RuleViolation("UPDATE must increment row_version")
       # if "UPDATED_AT" not in sql_upper:
        #    raise RuleViolation("UPDATE must update updated_at")
        

        for patter in TAUTOLOGIES:
            if re.search(patter,sql_upper):
                raise RuleViolation("Tautological WHERE clause detected")
            


            

