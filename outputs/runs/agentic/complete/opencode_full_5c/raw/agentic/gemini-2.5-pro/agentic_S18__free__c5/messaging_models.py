from pydantic import BaseModel
from typing import Optional, Dict, Any


class PubSubMessage(BaseModel):
    data: Dict[str, Any]
    attributes: Optional[Dict[str, str]] = None
