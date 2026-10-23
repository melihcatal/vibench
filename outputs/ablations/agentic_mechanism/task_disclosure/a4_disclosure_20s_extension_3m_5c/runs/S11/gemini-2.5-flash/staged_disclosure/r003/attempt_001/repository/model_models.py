
import json
from typing import Any, Dict, List, Union

class ManagedModelRequest:
    """
    Represents a standardized request format for the Managed Model Platform Workflow.
    """
    def __init__(self, data: Union[Dict, List]):
        self.data = data

    def to_json(self) -> str:
        return json.dumps(self.data)

    @classmethod
    def from_json(cls, json_str: str):
        return cls(json.loads(json_str))

class ManagedModelResponse:
    """
    Represents a standardized response format from the Managed Model Platform Workflow.
    """
    def __init__(self, predictions: Union[Dict, List], status: str = "success"):
        self.predictions = predictions
        self.status = status

    def to_json(self) -> str:
        return json.dumps({"predictions": self.predictions, "status": self.status})

    @classmethod
    def from_json(cls, json_str: str):
        data = json.loads(json_str)
        return cls(predictions=data.get("predictions"), status=data.get("status", "success"))

def normalize_data(data: Any) -> Any:
    """
    A helper function to normalize data before sending it to or after receiving it from
    the Managed Model Platform. This can include type conversions, scaling, etc.
    For this example, it simply returns the data as is, but can be extended.
    """
    # Example: If data is a pandas DataFrame, convert to list of dicts
    # if isinstance(data, pd.DataFrame):
    #     return data.to_dict(orient='records')
    # Example: Ensure all numbers are floats
    # if isinstance(data, (int, float)):
    #     return float(data)
    return data

