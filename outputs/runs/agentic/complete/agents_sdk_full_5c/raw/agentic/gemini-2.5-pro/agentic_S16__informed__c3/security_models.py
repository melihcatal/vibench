from dataclasses import dataclass
from typing import Optional, Dict, Any, List

@dataclass
class Secret:
    """A generic secret model."""
    name: str
    value: str
    version: Optional[str] = None
    provider: Optional[str] = None

@dataclass
class ApiKey(Secret):
    """Represents an API key secret."""
    service_name: str

@dataclass
class DatabaseCredentials:
    """Represents structured database credentials."""
    username: str
    password: str
    host: str
    port: int
    dbname: str
    engine: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DatabaseCredentials":
        return cls(
            username=data.get("username"),
            password=data.get("password"),
            host=data.get("host"),
            port=int(data.get("port", 5432)),
            dbname=data.get("dbname"),
            engine=data.get("engine"),
        )

@dataclass
class AuditRecord:
    """Represents a secret audit event."""
    secret_name: str
    event_time: str
    user: str
    action: str
    notes: str
    embedding: Optional[List[float]] = None
