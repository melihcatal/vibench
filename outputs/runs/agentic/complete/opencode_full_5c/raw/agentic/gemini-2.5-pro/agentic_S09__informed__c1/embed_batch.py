from typing import List
from embeddings_client import get_cohere_client
from embeddings_models import EmbeddingRequest, EmbeddingResponse


def generate_embeddings_batch(texts: List[str]):
    """
    Generates embeddings for a batch of text strings.
    """
    cohere_client = get_cohere_client()

    request = EmbeddingRequest(
        texts=texts, model="embed-english-v3.0", input_type="search_document"
    )

    response = cohere_client.embed(
        texts=request.texts, model=request.model, input_type=request.input_type
    )

    return EmbeddingResponse(embeddings=response.embeddings).embeddings


if __name__ == "__main__":
    # This is an example and will not be executed
    sample_texts = [
        "First text for batch embedding.",
        "Second text for batch embedding.",
        "Third text goes here.",
    ]
    embedding_vectors = generate_embeddings_batch(sample_texts)
    print(f"Number of vectors: {len(embedding_vectors)}")
    print(f"Length of first vector: {len(embedding_vectors[0])}")
