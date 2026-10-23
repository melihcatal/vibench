
import dataclasses
from typing import Any, Dict, List, Optional

@dataclasses.dataclass
class RequestModel:
    """
    Represents a request for the Managed Model Platform Workflow.
    Add specific fields as per the workflow requirements.
    """
    data: Dict[str, Any]
    model_id: str
    version: str = "1.0"

@dataclasses.dataclass
class ResponseModel:
    """
    Represents a response from the Managed Model Platform Workflow.
    Add specific fields as per the workflow requirements.
    """
    prediction: Any
    model_id: str
    status: str = "success"
    message: Optional[str] = None

def normalize_data(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalizes input data for the Managed Model Platform Workflow.
    Implement specific normalization logic here.
    """
    # Example: Basic normalization (e.g., lowercasing keys, handling missing values)
    normalized = {k.lower(): v for k, v in input_data.items()}
    return normalized

