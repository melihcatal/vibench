from pydantic import BaseModel
from typing import Any

class Event(BaseModel):
    id: str
    type: str
    data: Any
