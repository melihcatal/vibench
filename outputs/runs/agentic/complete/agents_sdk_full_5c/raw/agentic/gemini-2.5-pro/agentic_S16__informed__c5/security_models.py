"""Local helper models for Secret Management."""
from typing import Optional
from pydantic import BaseModel, Field


class DatabaseCredentials(BaseModel):
    """Represents the structure of a JSON secret for database credentials."""
    username: str
    password: str
    host: str
    port: int
    dbname: str
    engine: Optional[str] = Field(default="postgres")
