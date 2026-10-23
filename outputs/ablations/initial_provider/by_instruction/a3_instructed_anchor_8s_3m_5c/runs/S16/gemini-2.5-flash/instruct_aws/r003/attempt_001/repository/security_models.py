from dataclasses import dataclass
from typing import Optional, Dict, Any

@dataclass
class Secret:
    name: str
    arn: str
    secret_string: Optional[str] = None
    secret_binary: Optional[bytes] = None
    version_id: Optional[str] = None
    created_date: Optional[Any] = None # datetime object
    tags: Optional[Dict[str, str]] = None
