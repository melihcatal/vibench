from pydantic import BaseModel

class LogRequest(BaseModel):
    logGroupName: str
    logStreamName: str
    logEvents: list

class LogResponse(BaseModel):
    nextSequenceToken: str

class QueryRequest(BaseModel):
    logGroupName: str
    startTime: int
    endTime: int
    queryString: str

class QueryResponse(BaseModel):
    results: list
    statistics: dict
    status: str