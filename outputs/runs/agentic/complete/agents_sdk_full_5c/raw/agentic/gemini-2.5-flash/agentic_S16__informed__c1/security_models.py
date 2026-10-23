from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any, List

@dataclass
class SecretVersion:
    name: str
    state: str
    create_time: datetime
    destroy_time: Optional[datetime] = None

@dataclass
class Secret:
    name: str
    labels: Dict[str, str]
    create_time: datetime
    versions: List[SecretVersion] = field(default_factory=list)

@dataclass
class ParsedJsonSecret:
    secret_id: str
    data: Dict[str, Any]
