from typing import Dict, Any, List

class LLMRequest:
    def __init__(self, prompt: str, temperature: float = 0.7, max_output_tokens: int = 1024):
        self.prompt = prompt
        self.temperature = temperature
        self.max_output_tokens = max_output_tokens

    def to_dict(self) -> Dict[str, Any]:
        return {
            "prompt": self.prompt,
            "temperature": self.temperature,
            "max_output_tokens": self.max_output_tokens,
        }

class LLMResponse:
    def __init__(self, text: str, safety_attributes: Dict[str, Any] = None):
        self.text = text
        self.safety_attributes = safety_attributes or {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "text": self.text,
            "safety_attributes": self.safety_attributes,
        }

class EmbeddingRequest:
    def __init__(self, texts: List[str]):
        self.texts = texts

    def to_dict(self) -> Dict[str, Any]:
        return {
            "instances": [{'content': text} for text in self.texts]
        }

class EmbeddingResponse:
    def __init__(self, embeddings: List[List[float]]):
        self.embeddings = embeddings

    def to_dict(self) -> Dict[str, Any]:
        return {
            "embeddings": self.embeddings
        }
