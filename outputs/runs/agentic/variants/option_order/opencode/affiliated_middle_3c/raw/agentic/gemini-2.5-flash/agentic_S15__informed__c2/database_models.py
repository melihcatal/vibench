from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass
class Document:
    collection_name: str
    id: str
    data: Dict[str, Any]
