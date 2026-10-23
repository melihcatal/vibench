from embeddings_client import get_cohere_client
from embeddings_models import EmbeddingRequest


def generate_embedding(text: str):
    """
    Generates an embedding vector for a single text string.
    """
    cohere_client = get_cohere_client()

    request = EmbeddingRequest(
        texts=[text], model="embed-english-v3.0", input_type="search_document"
    )

    response = cohere_client.embed(
        texts=request.texts, model=request.model, input_type=request.input_type
    )

    return response.embeddings[0]


if __name__ == "__main__":
    # This is an example and will not be executed
    sample_text = "This is a test sentence for embedding."
    embedding_vector = generate_embedding(sample_text)
    print(f"Embedding vector length: {len(embedding_vector)}")
