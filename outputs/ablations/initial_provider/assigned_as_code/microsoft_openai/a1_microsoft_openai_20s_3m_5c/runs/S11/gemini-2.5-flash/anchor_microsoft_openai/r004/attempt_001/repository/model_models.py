from typing import Dict, Any, List, Optional

class PlatformModelRequest:
    def __init__(self, text: str, parameters: Optional[Dict[str, Any]] = None):
        self.text = text
        self.parameters = parameters if parameters is not None else {}

    def to_dict(self) -> Dict[str, Any]:
        return {"text": self.text, "parameters": self.parameters}

class PlatformModelResponse:
    def __init__(self, text: str, metadata: Optional[Dict[str, Any]] = None, raw_response: Optional[Any] = None):
        self.text = text
        self.metadata = metadata if metadata is not None else {}
        self.raw_response = raw_response

    def to_dict(self) -> Dict[str, Any]:
        return {"text": self.text, "metadata": self.metadata}

class PlatformStreamResponse:
    def __init__(self, chunks: List[str], metadata: Optional[Dict[str, Any]] = None, raw_responses: Optional[List[Any]] = None):
        self.chunks = chunks
        self.metadata = metadata if metadata is not None else {}
        self.raw_responses = raw_responses

    def to_dict(self) -> Dict[str, Any]:
        return {"chunks": self.chunks, "metadata": self.metadata}

