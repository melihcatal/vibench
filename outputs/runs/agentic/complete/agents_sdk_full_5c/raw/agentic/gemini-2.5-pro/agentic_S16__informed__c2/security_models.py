from pydantic import BaseModel, Field

class ApiKey(BaseModel):
    """
    Represents a generic API key secret.
    """
    key: str = Field(..., alias="api_key")

class DatabaseCredentials(BaseModel):
    """
    Represents database connection credentials.
    """
    username: str
    password: str
    host: str
    port: int
    dbname: str
    engine: str
