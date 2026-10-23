from pydantic import BaseModel

class Document(BaseModel):
    _id: str
    data: dict