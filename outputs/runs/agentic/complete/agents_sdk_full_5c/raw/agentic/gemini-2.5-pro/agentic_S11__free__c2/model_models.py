from dataclasses import dataclass, field
from typing import Any, Dict, Optional

@dataclass
class ModelRequest:
    """Represents a request to the model platform."""
    prompt: str
    model: str = "command-r"

@dataclass
class ModelResponse:
    """Represents a response from the model platform, including metadata."""
    text: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    provider_response: Optional[Any] = None
