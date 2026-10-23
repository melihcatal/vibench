from pydantic import BaseModel

class LogEvent(BaseModel):
    timestamp: int
    message: str

class LogQuery(BaseModel):
    logGroupName: str
    startTime: int
    endTime: int
    queryString: str