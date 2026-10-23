from pydantic import BaseModel

class ModerationRequest(BaseModel):
    text: str

class ModerationResponse(BaseModel):
    is_safe: bool
    categories: dict