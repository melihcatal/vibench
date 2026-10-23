from typing import Any, Dict, List

from amazon_nova_api import NovaEmbeddingsClient


class EmbeddingRequest:
    def __init__(self, texts: List[str]):
        self.texts = texts

    def to_dict(self) -> Dict[str, Any]:
        return {"texts": self.texts}


class EmbeddingResponse:
    def __init__(self, embeddings: List[List[float]]):
        self.embeddings = embeddings

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "EmbeddingResponse":
        return cls(embeddings=data["embeddings"])


def normalize_embeddings(embeddings: List[List[float]]) -> List[List[float]]:
    # Normalization logic here
    return embeddings


def get_embeddings_client() -> NovaEmbeddingsClient:
    return NovaEmbeddingsClient(model_id='amazon-nova-api/nova-pro-v1')