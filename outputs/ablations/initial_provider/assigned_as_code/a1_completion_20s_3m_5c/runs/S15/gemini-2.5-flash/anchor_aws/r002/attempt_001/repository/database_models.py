import json
from decimal import Decimal
from typing import Any, Dict, Optional

import pydantic


class Document(pydantic.BaseModel):
    id: str
    document: Dict[str, Any]
    key_field: Optional[str] = "id"


class DocumentQuery(pydantic.BaseModel):
    table_name: str
    key_field: str
    key_value: str


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        return json.JSONEncoder.default(self, obj)
