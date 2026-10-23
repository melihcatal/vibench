import dataclasses
from typing import Dict, Any, List


@dataclasses.dataclass
class DocumentInput:
    content: bytes
    mime_type: str


@dataclasses.dataclass
class DocumentOutput:
    text: str = ""
    entities: List[Dict[str, Any]] = dataclasses.field(default_factory=list)
    pages: List[Dict[str, Any]] = dataclasses.field(default_factory=list)
    tables: List[Dict[str, Any]] = dataclasses.field(default_factory=list)
    key_value_pairs: List[Dict[str, Any]] = dataclasses.field(default_factory=list)
