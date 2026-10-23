from pydantic import BaseModel

class LogData(BaseModel):
    time: str
    severity: str
    message: str

class CorrelatedLogData(BaseModel):
    time: str
    severity: str
    message: str
    correlationId: str
