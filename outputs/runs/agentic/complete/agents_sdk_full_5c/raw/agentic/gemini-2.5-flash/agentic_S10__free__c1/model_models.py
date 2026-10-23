from typing import List, Dict, Any, Optional

class LLMRequest:
    """
    A simple class to represent a generic LLM request.
    """
    def __init__(self, prompt: str, model: str = "gemini-pro", temperature: float = 0.7, max_output_tokens: int = 1024):
        self.prompt = prompt
        self.model = model
        self.temperature = temperature
        self.max_output_tokens = max_output_tokens

    def to_dict(self) -> Dict[str, Any]:
        return {
            "prompt": self.prompt,
            "model": self.model,
            "temperature": self.temperature,
            "max_output_tokens": self.max_output_tokens,
        }

class LLMResponse:
    """
    A simple class to represent a generic LLM response.
    """
    def __init__(self, text: str, safety_attributes: Optional[Dict[str, Any]] = None, finish_reason: Optional[str] = None):
        self.text = text
        self.safety_attributes = safety_attributes if safety_attributes is not None else {}
        self.finish_reason = finish_reason
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "text": self.text,
            "safety_attributes": self.safety_attributes,
            "finish_reason": self.finish_reason,
        }

class EmbeddingRequest:
    """
    A simple class to represent an embedding request.
    """
    def __init__(self, texts: List[str], model: str = "embedding-001"):
        self.texts = texts
        self.model = model

class EmbeddingResponse:
    """
    A simple class to represent an embedding response.
    """
    def __init__(self, embeddings: List[List[float]], model: str = "embedding-001"):
        self.embeddings = embeddings
        self.model = model
