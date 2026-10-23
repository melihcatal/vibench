from typing import Dict, List

from direct_embeddings_sdk import DirectEmbeddingsClient


class EmbeddingRequest:
    def __init__(self, texts: List[str]):
        self.texts = texts

    def to_dict(self) -> Dict[str, List[str]]:
        return {'texts': self.texts}


class EmbeddingResponse:
    def __init__(self, embeddings: List[List[float]]):
        self.embeddings = embeddings

    @classmethod
    def from_dict(cls, data: Dict[str, List[List[float]]]) -> 'EmbeddingResponse':
        return cls(embeddings=data['embeddings'])


def normalize_embeddings(embeddings: List[List[float]]) -> List[List[float]]:
    normalized_embeddings = []
    for embedding in embeddings:
        norm = sum([e ** 2 for e in embedding]) ** 0.5
        normalized_embeddings.append([e / norm for e in embedding])
    return normalized_embeddings
