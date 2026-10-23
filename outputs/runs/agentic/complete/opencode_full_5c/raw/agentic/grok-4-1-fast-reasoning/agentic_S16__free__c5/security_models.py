from dataclasses import dataclass
from typing import List, Optional


@dataclass
class SecretResponse:
    value: str
    version_id: str
    version_stages: List[str]
    created_date: Optional[str] = None
