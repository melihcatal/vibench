from dataclasses import dataclass, field
from typing import Any, Dict

@dataclass
class GenerationResult:
    """A standard container for model generation results."""
    text: str
    metadata: Dict[str, Any] = field(default_factory=dict)
