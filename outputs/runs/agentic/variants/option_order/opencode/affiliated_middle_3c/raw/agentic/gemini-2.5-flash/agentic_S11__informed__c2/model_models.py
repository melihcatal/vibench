from typing import Dict, Any


class ModelRequest:
    def __init__(self, prompt: str, **kwargs):
        self.prompt = prompt
        self.params = kwargs


class ModelResponse:
    def __init__(self, text: str, metadata: Dict[str, Any] = None):
        self.text = text
        self.metadata = metadata if metadata is not None else {}
