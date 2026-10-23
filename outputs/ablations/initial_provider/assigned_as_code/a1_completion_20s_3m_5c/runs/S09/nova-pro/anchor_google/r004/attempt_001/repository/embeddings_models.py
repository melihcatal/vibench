from typing import List, Dict


class EmbeddingRequest:
    def __init__(self, texts: List[str]):
        self.texts = texts

    def to_dict(self) -> Dict:
        return {'texts': self.texts}


class EmbeddingResponse:
    def __init__(self, embeddings: List[Dict]):
        self.embeddings = embeddings

    @classmethod
    def from_dict(cls, data: Dict) -> 'EmbeddingResponse':
        return cls(embeddings=data['embeddings'])