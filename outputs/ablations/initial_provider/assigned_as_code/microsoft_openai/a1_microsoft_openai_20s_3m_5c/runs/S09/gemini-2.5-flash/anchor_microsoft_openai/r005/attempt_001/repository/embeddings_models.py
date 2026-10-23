from typing import List, Dict, Any


class EmbeddingRequest:
    def __init__(self, texts: List[str], model: str = 'text-embedding-3-small'):
        self.texts = texts
        self.model = model

    def to_openai_payload(self) -> Dict[str, Any]:
        return {
            'input': self.texts,
            'model': self.model,
        }


class EmbeddingResponse:
    def __init__(self, openai_response: Any):
        self.embeddings = [item.embedding for item in openai_response.data]
        self.model = openai_response.model

    def to_dict(self) -> Dict[str, Any]:
        return {
            'embeddings': self.embeddings,
            'model': self.model,
        }