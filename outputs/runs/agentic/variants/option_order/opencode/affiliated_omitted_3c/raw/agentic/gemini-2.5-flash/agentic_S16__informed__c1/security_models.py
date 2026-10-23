from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class SecretValue:
    """
    A basic dataclass to represent a secret value.
    """

    name: str
    value: str
    arn: Optional[str] = None
    version_id: Optional[str] = None
    created_date: Optional[Any] = None
