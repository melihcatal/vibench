
from pydantic import BaseModel, SecretStr

class DatabaseCredentials(BaseModel):
    """
    A Pydantic model to represent structured database credentials
    retrieved from a secret store.
    """
    username: str
    password: SecretStr
    host: str
    port: int
    dbname: str

class ApiKey(BaseModel):
    """
    A Pydantic model for a simple API key.
    """
    key: SecretStr
    service_name: str
