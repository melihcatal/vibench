from dataclasses import dataclass
from typing import Optional

@dataclass
class Secret:
    name: str
    value: str
    version: Optional[str] = None

@dataclass
class DatabaseCredentials:
    username: str
    password: str
    host: str
    port: int
    dbname: str
