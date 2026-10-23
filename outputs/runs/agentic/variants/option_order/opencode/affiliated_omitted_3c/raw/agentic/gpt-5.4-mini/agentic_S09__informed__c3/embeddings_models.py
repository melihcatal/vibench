from dataclasses import dataclass


@dataclass
class SingleEmbeddingRequest:
    text: str
    model: str


@dataclass
class BatchEmbeddingRequest:
    texts: list
    model: str


@dataclass
class SearchEmbeddingRequest:
    query: str
    documents: list
    model: str


def normalize_embedding_result(response, single_text=None):
    embeddings = getattr(response, "embeddings", None)
    if embeddings is None:
        embeddings = getattr(response, "embeddings", [])
    if hasattr(embeddings, "float"):
        embeddings = embeddings.float
    if single_text is not None and embeddings and len(embeddings) == 1:
        return [list(embeddings[0])]
    return [list(item) for item in embeddings]

