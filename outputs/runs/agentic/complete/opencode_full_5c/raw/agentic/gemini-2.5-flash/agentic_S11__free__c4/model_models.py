from typing import List, Dict, Any


class ModelRequest:
    """Represents a generic model request."""

    def __init__(self, prompt: str, **kwargs):
        self.prompt = prompt
        self.kwargs = kwargs


class ModelResponse:
    """Represents a generic model response."""

    def __init__(
        self, text: str, raw_response: Dict[str, Any], metadata: Dict[str, Any] = None
    ):
        self.text = text
        self.raw_response = raw_response
        self.metadata = metadata if metadata is not None else {}
