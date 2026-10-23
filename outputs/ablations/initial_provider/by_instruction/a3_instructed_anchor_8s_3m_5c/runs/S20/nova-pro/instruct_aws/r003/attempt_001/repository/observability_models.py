from pydantic import BaseModel

class LogEvent(BaseModel):
    timestamp: int
    message: str

class LogResponse(BaseModel):
    events: list[LogEvent]
