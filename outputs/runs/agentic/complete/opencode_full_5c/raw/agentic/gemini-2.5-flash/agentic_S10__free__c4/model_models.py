from typing import List, Dict, Any


class LLMRequest:
    def __init__(self, prompt: str, model_id: str = "gemini-pro"):
        self.prompt = prompt
        self.model_id = model_id


class LLMContextRequest(LLMRequest):
    def __init__(self, prompt: str, context: str, model_id: str = "gemini-pro"):
        super().__init__(prompt, model_id)
        self.context = context


class LLMResponse:
    def __init__(self, text: str, model_id: str):
        self.text = text
        self.model_id = model_id


class EmbeddingRequest:
    def __init__(self, texts: List[str], model_id: str = "text-embedding-004"):
        self.texts = texts
        self.model_id = model_id


class EmbeddingResponse:
    def __init__(self, embeddings: List[List[float]], model_id: str):
        self.embeddings = embeddings
        self.model_id = model_id
