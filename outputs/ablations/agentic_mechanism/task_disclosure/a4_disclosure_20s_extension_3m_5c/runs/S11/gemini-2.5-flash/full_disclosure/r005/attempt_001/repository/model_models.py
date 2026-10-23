import dataclasses
from typing import Any, Dict, List, Optional

@dataclasses.dataclass
class PlatformModelRequest:
    """
    Represents a standardized request structure for invoking a managed model platform.
    This can encapsulate various input formats specific to a provider like Google Cloud Vertex AI.
    """
    instances: List[Dict[str, Any]]
    parameters: Optional[Dict[str, Any]] = None
    model_id: Optional[str] = None
    endpoint_id: Optional[str] = None

@dataclasses.dataclass
class PlatformModelResponse:
    """
    Represents a standardized response structure from a managed model platform.
    This can encapsulate various output formats specific to a provider like Google Cloud Vertex AI.
    """
    predictions: List[Dict[str, Any]]
    deployed_model_id: Optional[str] = None
    model: Optional[str] = None

def normalize_platform_response(raw_response: Dict[str, Any]) -> PlatformModelResponse:
    """
    Normalizes a raw response from a managed model platform into a standardized PlatformModelResponse.
    This function handles variations in provider-specific response formats, for instance, from Google Cloud Vertex AI.
    """
    predictions = raw_response.get("predictions", [])
    deployed_model_id = raw_response.get("deployedModelId")
    model = raw_response.get("model")
    
    return PlatformModelResponse(
        predictions=predictions,
        deployed_model_id=deployed_model_id,
        model=model
    )
