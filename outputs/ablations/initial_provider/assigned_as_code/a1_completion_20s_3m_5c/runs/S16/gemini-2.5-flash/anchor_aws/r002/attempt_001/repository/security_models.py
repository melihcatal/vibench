from dataclasses import dataclass
from typing import Optional, Dict, Any

@dataclass
class SecretPayload:
    secret_id: str
    key_field: Optional[str] = None
    version_id: Optional[str] = None
    version_stage: Optional[str] = None

@dataclass
class DBSecret:
    username: str
    password: str
    host: str
    port: int
    dbname: str

@dataclass
class ParsedSecret:
    parsed_secret: Dict[str, Any]
