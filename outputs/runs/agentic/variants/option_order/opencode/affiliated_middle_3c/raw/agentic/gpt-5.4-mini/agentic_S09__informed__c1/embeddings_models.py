from dataclasses import dataclass


@dataclass
class EmbeddingRequest:
    input_texts: list[str]
    model: str


def extract_embedding_vector(response, index: int = 0):
    return response.data[index].embedding


def extract_embeddings_vectors(response):
    return [item.embedding for item in response.data]
