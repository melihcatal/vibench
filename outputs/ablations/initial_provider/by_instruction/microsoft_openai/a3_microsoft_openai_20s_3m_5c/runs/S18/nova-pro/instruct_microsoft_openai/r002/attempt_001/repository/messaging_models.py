from pydantic import BaseModel

class Event(BaseModel):
    id: str
    attributes: dict
    payload: dict

class Message(BaseModel):
    id: str
    attributes: dict
    payload: dict