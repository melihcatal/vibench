from typing import Dict, Any, Optional


class ModelRequest:
    def __init__(self, prompt: str, **kwargs):
        self.prompt = prompt
        self.kwargs = kwargs


class ModelResponse:
    def __init__(self, text: str, metadata: Optional[Dict[str, Any]] = None):
        self.text = text
        self.metadata = metadata if metadata is not None else {}

    def __str__(self):
        return self.text
