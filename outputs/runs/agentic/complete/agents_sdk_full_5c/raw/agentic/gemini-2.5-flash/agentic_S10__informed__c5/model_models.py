from typing import List, Dict, Any, Optional

class LLMRequest:
    def __init__(self, prompt: str, model: str = "gemini-pro", temperature: float = 0.7, max_output_tokens: int = 1024):
        self.prompt = prompt
        self.model = model
        self.temperature = temperature
        self.max_output_tokens = max_output_tokens

class LLMResponse:
    def __init__(self, text: Optional[str] = None, json_output: Optional[Dict[str, Any]] = None, raw_response: Optional[Any] = None):
        self.text = text
        self.json_output = json_output
        self.raw_response = raw_response

class EmbeddingRequest:
    def __init__(self, text: str, model: str = "embedding-001"):
        self.text = text
        self.model = model

class EmbeddingResponse:
    def __init__(self, embedding: List[float], raw_response: Optional[Any] = None):
        self.embedding = embedding
        self.raw_response = raw_response
