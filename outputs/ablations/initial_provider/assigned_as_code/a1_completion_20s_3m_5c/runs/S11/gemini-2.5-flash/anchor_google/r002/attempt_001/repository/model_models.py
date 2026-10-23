from dataclasses import dataclass
from typing import Any, Dict

@dataclass
class PlatformModelRequest:
    text_content: str
    parameters: Dict[str, Any] | None = None

def normalize_response(response_object: Any) -> Dict[str, Any]:
    # This is a placeholder for actual normalization logic
    # In a real scenario, this would parse the provider's response object
    # into a consistent format.
    return {
        "text": response_object.text or "",
        "raw_data": response_object.to_dict() if hasattr(response_object, 'to_dict') else str(response_object)
    }
