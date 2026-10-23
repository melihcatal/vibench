from typing import Any, Dict


class ModelRequest:
    def __init__(self, prompt: str, model: str):
        self.prompt = prompt
        self.model = model


class ModelResponse:
    def __init__(self, text: str, metadata: Dict[str, Any]):
        self.text = text
        self.metadata = metadata
