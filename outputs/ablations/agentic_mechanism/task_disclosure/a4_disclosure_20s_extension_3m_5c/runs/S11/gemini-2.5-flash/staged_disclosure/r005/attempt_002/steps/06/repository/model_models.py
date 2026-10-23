
import json
from typing import Any, Dict, List, Optional

class ModelRequest:
    """
    Represents a request to the Managed Model Platform.
    """
    def __init__(self, model_id: str, data: Dict[str, Any], version: str = "v1"):
        self.model_id = model_id
        self.data = data
        self.version = version

    def to_json(self) -> str:
        return json.dumps({
            "model_id": self.model_id,
            "version": self.version,
            "data": self.data
        })

    @classmethod
    def from_json(cls, json_str: str):
        data = json.loads(json_str)
        return cls(
            model_id=data["model_id"],
            data=data["data"],
            version=data.get("version", "v1")
        )

class ModelResponse:
    """
    Represents a response from the Managed Model Platform.
    """
    def __init__(self, model_id: str, predictions: List[Any], status: str = "success", error: Optional[str] = None):
        self.model_id = model_id
        self.predictions = predictions
        self.status = status
        self.error = error

    def to_json(self) -> str:
        return json.dumps({
            "model_id": self.model_id,
            "predictions": self.predictions,
            "status": self.status,
            "error": self.error
        })

    @classmethod
    def from_json(cls, json_str: str):
        data = json.loads(json_str)
        return cls(
            model_id=data["model_id"],
            predictions=data["predictions"],
            status=data.get("status", "success"),
            error=data.get("error")
        )

def normalize_data(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalizes input data for the Managed Model Platform.
    This is a placeholder for actual normalization logic.
    """
    # Example normalization: ensure all string values are stripped of whitespace
    normalized = {}
    for key, value in input_data.items():
        if isinstance(value, str):
            normalized[key] = value.strip()
        else:
            normalized[key] = value
    return normalized

