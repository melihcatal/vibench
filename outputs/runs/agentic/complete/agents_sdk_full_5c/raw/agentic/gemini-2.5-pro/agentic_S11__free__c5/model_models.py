from dataclasses import dataclass, field
from typing import Any, Dict

@dataclass
class ModelRequest:
    """Represents a simple request to the model."""
    prompt: str

@dataclass
class ModelResponseWithMetadata:
    """Represents a model response including provider metadata."""
    text: str
    metadata: Dict[str, Any] = field(default_factory=dict)
