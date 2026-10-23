from pydantic import BaseModel

class Document(BaseModel):
    id: str
    data: dict

class Update(BaseModel):
    op: str
    path: str
    value: any

class Condition(BaseModel):
    op: str
    path: str
    value: any