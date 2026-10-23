from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List


class Document(BaseModel):
    id: str
    content: Dict[str, Any]
    partition_key: Optional[str] = None


class QueryResult(BaseModel):
    items: List[Dict[str, Any]]
    continuation_token: Optional[str] = None
