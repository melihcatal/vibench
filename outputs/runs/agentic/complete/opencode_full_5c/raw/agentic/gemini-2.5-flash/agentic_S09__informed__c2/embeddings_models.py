from typing import List, Dict


class EmbeddingRequest:
    def __init__(self, texts: List[str]):
        self.texts = texts


class EmbeddingResponse:
    def __init__(self, embeddings: List[List[float]]):
        self.embeddings = embeddings


def normalize_embedding_response(response) -> EmbeddingResponse:
    # Google Generative AI SDK returns a BatchEmbedContentsResponse object
    # We extract the embeddings from it.
    embeddings_list = [item.values for item in response.embeddings]
    return EmbeddingResponse(embeddings_list)
