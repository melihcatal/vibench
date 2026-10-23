from pydantic import BaseModel
from typing import Optional


class SecretData(BaseModel):
    username: str
    password: str
    host: str
    port: int
    database: str
    api_key: Optional[str] = None
