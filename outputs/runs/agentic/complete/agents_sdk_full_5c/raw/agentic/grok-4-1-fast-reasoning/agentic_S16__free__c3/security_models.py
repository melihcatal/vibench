from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class DBConnectionSecret(BaseModel):
    host: str
    port: Optional[int] = 5432
    username: str
    password: str
    database: str