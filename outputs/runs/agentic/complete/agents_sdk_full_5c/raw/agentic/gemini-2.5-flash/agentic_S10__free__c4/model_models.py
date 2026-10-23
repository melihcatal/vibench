from typing import List, Dict, Any

class LLMRequest:
    def __init__(self, prompt: str, **kwargs):
        self.prompt = prompt
        self.kwargs = kwargs

class LLMResponse:
    def __init__(self, text: str, raw_response: Any = None):
        self.text = text
        self.raw_response = raw_response

class EmbeddingRequest:
    def __init__(self, texts: List[str]):
        self.texts = texts

class EmbeddingResponse:
    def __init__(self, embeddings: List[List[float]], raw_response: Any = None):
        self.embeddings = embeddings
        self.raw_response = raw_response
