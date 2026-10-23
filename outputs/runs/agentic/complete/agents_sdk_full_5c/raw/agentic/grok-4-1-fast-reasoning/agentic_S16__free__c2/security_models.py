from dataclasses import dataclass
from typing import Dict, Any, Optional, List

@dataclass
class SecretResponse:
    name: str
    value: str
    version: Optional[int] = None

@dataclass
class DbSecret:
    host: str
    port: int
    username: str
    password: str

@dataclass
class AuditLog:
    timestamp: str
    message: str
    notes: Optional[str] = None