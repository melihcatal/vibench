from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class ModelRequest:
    prompt: str
    parameters: Optional[Dict[str, Any]] = None


@dataclass
class ModelResponse:
    text: str
    metadata: Optional[Dict[str, Any]] = None
