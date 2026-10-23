from typing import List, Dict, Any


def normalize_embedding(embedding: List[float]) -> List[float]:
    norm = sum(x * x for x in embedding) ** 0.5
    if norm == 0:
        return embedding
    return [x / norm for x in embedding]


class EmbeddingRequest:
    def __init__(
        self,
        texts: List[str],
        model: str = "embed-english-v3.0",
        input_type: str = "search_document",
    ):
        self.texts = texts
        self.model = model
        self.input_type = input_type

    def to_dict(self) -> Dict[str, Any]:
        return {
            "texts": self.texts,
            "model": self.model,
            "input_type": self.input_type,
        }


class EmbeddingResponse:
    def __init__(self, embeddings: List[List[float]]):
        self.embeddings = embeddings

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "EmbeddingResponse":
        return cls(embeddings=data.get("embeddings", []))
