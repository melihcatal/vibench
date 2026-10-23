from pydantic import BaseModel

class LogEntry(BaseModel):
    timestamp: str
    level: str
    message: str
    userId: str
    correlationId: str = None

class LogEventResponse(BaseModel):
    status: str
    message: str