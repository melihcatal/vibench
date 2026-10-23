import os
from observability_client import get_embedding_model_client
from observability_models import EmbeddingRequest, EmbeddingResponse


def embed_log_message(request: EmbeddingRequest) -> EmbeddingResponse:
    """
    Embeds a log message for semantic retrieval using Google's text embedding model.
    """
    model = get_embedding_model_client(model_name="textembedding-gecko@003")

    embeddings = model.get_embeddings([request.text])

    if not embeddings:
        raise ValueError("Failed to get embedding for the provided text.")

    embedding_vector = embeddings[0].values
    return EmbeddingResponse(embedding=embedding_vector)


if __name__ == "__main__":
    if os.environ.get("GCP_PROJECT_ID"):
        log_message = "Database query failed due to a unique constraint violation."
        request = EmbeddingRequest(text=log_message)

        response = embed_log_message(request)

        print(f"Original message: {log_message}")
        print(f"Embedding vector (first 10 dims): {response.embedding[:10]}")
        print(f"Total dimensions: {len(response.embedding)}")
    else:
        print("GCP_PROJECT_ID environment variable not set. Skipping example run.")
