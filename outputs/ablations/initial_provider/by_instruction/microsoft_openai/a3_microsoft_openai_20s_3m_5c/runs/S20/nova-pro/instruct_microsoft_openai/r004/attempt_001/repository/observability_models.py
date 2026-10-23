from pydantic import BaseModel

class LogData(BaseModel):
    time: str
    level: str
    message: str
    correlation_id: str = None

class QueryResponse(BaseModel):
    tables: list
