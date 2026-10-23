from typing import Any, Dict, List, Optional

class ModelRequest:
    def __init__(self, text: str, config: Optional[Dict[str, Any]] = None):
        self.text = text
        self.config = config or {}

class ModelResponse:
    def __init__(self, text: str, metadata: Optional[Dict[str, Any]] = None):
        self.text = text
        self.metadata = metadata or {}
