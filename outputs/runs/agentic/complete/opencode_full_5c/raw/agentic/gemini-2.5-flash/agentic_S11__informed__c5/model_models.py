from typing import Any, Dict, List, Optional


class PlatformModelRequest:
    def __init__(
        self,
        prompt: str,
        model_id: Optional[str] = None,
        parameters: Optional[Dict[str, Any]] = None,
    ):
        self.prompt = prompt
        self.model_id = model_id
        self.parameters = parameters or {}


class PlatformModelResponse:
    def __init__(self, text: str, metadata: Optional[Dict[str, Any]] = None):
        self.text = text
        self.metadata = metadata or {}


class PlatformStreamResponse:
    def __init__(self, chunks: List[str], metadata: Optional[Dict[str, Any]] = None):
        self.chunks = chunks
        self.metadata = metadata or {}
