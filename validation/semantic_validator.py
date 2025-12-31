from enum import Enum

class RiskLevel(str,Enum):


    LOW="LOW"
    MEDIUM="MEDIUM"
    HIGH="HIGH"



def semantic_validate(
        operation:str,
        table:str,
        columns_written:list,
        row_count: int
)->dict:
    risk_score=0

    warnings=[]

    if operation in {"UPDATE","DELETE"}:
        risk_score+=2

    if row_count>100:
        risk_score+=3
        warnings.append("Large number of rows affected")


    if "role" in columns_written or "password" in columns_written:
        risk_score+=4
        warnings.append("Sensitive column modification")


    if risk_score>=6:
        risk=RiskLevel.HIGH
    

    elif risk_score>=3:
        risk=RiskLevel.MEDIUM


    else:
        risk=RiskLevel.LOW

    return{
        "risk":risk,
        "warnings":warnings,
    }

