from dataclasses import dataclass
from typing import Dict, Any, Optional

@dataclass
class ApiKeySecret:
    api_key: str

@dataclass
class DbSecret:
    host: str
    port: str
    username: str
    password: str
    database: Optional[str] = None

JsonSecret = Dict[str, Any]