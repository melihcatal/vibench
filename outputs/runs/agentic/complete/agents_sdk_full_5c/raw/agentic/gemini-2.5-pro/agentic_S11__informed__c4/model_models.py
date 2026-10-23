from dataclasses import dataclass
from typing import Any, Dict, Optional

@dataclass
class ModelRequest:
    """Represents a request to the model."""
    prompt: str

@dataclass
class ModelResponse:
    """Represents a response from the model, including metadata."""
    text: Optional[str]
    metadata: Dict[str, Any]
