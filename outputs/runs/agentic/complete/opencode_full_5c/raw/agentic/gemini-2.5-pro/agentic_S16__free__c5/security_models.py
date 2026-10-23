from pydantic import BaseModel


class DatabaseSecret(BaseModel):
    username: str
    password: str
    engine: str
    host: str
    port: int
    dbname: str
