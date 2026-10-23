from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Any


@dataclass
class SecretInfo:
    name: str
    labels: Dict[str, str]
    notes: str
    rotation_status: Optional[str] = None
