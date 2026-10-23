import dataclasses
from typing import List, Dict, Any, Optional


@dataclasses.dataclass
class DocumentInput:
    content: bytes
    mime_type: str
    file_extension: str


@dataclasses.dataclass
class DocumentOutput:
    text: Optional[str] = None
    entities: Optional[List[Dict[str, Any]]] = None
    pages: Optional[List[Dict[str, Any]]] = None
    tables: Optional[List[Dict[str, Any]]] = None
    key_value_pairs: Optional[List[Dict[str, Any]]] = None
