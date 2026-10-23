from dataclasses import dataclass


@dataclass
class EmbeddingRequest:
    input: object
    model: str


def normalize_embedding_response(response):
    data = getattr(response, "data", response)
    vectors = []
    for item in data:
        embedding = getattr(item, "embedding", item.get("embedding"))
        vectors.append(list(embedding))
    return vectors
