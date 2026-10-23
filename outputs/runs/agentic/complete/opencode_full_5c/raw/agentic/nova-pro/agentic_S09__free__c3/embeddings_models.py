from dataclasses import dataclass


@dataclass
class EmbeddingsRequest:
    text: str


@dataclass
class EmbeddingsBatchRequest:
    texts: list


@dataclass
class EmbeddingsResponse:
    embeddings: list
