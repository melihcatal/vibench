from typing import Dict, Any, Optional, Iterator
from pydantic import BaseModel


class WatsonXRequest(BaseModel):
    model_id: str
    input: str
    params: Dict[str, Any]


class WatsonXResponse(BaseModel):
    output: str


def normalize_model_id(model_id: str) -> str:
    """Normalize WatsonX model ID to full format."""
    if not model_id.startswith("ibm/"):
        return f"ibm/{model_id}"
    return model_id
