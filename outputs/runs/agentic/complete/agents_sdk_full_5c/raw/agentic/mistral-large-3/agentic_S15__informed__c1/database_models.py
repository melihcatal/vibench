from pydantic import BaseModel
from typing import Dict, Optional

class DocumentRequest(BaseModel):
    data: Dict

class DocumentResponse(BaseModel):
    id: str
    data: Dict

class QueryRequest(BaseModel):
    field: str
    value: str

class ConditionalUpdateRequest(BaseModel):
    update_data: Dict
    condition_field: str
    condition_value: str