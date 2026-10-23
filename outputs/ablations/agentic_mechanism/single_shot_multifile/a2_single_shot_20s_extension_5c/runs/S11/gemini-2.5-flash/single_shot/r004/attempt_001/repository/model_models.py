from typing import Dict, Any, List

class ModelRequest:
    def __init__(self, prompt: str, parameters: Dict[str, Any] = None):
        self.prompt = prompt
        self.parameters = parameters if parameters is not None else {}

    def to_dict(self) -> Dict[str, Any]:
        return {"prompt": self.prompt, "parameters": self.parameters}

class ModelResponse:
    def __init__(self, text_output: str, raw_response: Any = None, metadata: Dict[str, Any] = None):
        self.text_output = text_output
        self.raw_response = raw_response
        self.metadata = metadata if metadata is not None else {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "text_output": self.text_output,
            "metadata": self.metadata
        }

class EmbeddingResponse:
    def __init__(self, embeddings: List[List[float]], raw_response: Any = None):
        self.embeddings = embeddings
        self.raw_response = raw_response

    def to_dict(self) -> Dict[str, Any]:
        return {"embeddings": self.embeddings}