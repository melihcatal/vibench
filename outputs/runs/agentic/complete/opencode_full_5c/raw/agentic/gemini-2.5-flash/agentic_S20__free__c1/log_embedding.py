import os
from typing import List
from google.cloud import aiplatform
from observability_client import ObservabilityClient  # for conceptual integration
from observability_models import LogEmbeddingResult

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")
LOCATION = "us-central1"  # Example region for Vertex AI


def embed_log_message(log_message: str) -> LogEmbeddingResult:
    aiplatform.init(project=PROJECT_ID, location=LOCATION)

    # Using a pre-trained embedding model
    # Provider Identification: aiplatform.TextEmbeddingModel.from_pretrained and specific model_id
    model = aiplatform.TextEmbeddingModel.from_pretrained(
        "text-embedding-004"
    )  # or "textembedding-gecko@001"

    print(f'Embedding log message: "{log_message}" ')

    # The predict method returns a list of embeddings
    embeddings = model.predict([log_message]).embeddings
    embedding_vector = []
    if embeddings:
        # Each embedding object has a values attribute which is a list of floats
        embedding_vector = embeddings[0].values

    return LogEmbeddingResult(
        original_message=log_message, embedding_vector=embedding_vector
    )


if __name__ == "__main__":
    # Example usage:
    message1 = "Database connection error: Could not connect to host."
    message2 = "Failed to establish database connection."
    message3 = "User logged out successfully."

    embedding1 = embed_log_message(message1)
    print(f'\n--- Embedding for "{embedding1.original_message}" ---')
    print(f"Embedding vector (first 5 elements): {embedding1.embedding_vector[:5]}...")
    print(f"Vector length: {len(embedding1.embedding_vector)}")

    embedding2 = embed_log_message(message2)
    print(f'\n--- Embedding for "{embedding2.original_message}" ---')
    print(f"Embedding vector (first 5 elements): {embedding2.embedding_vector[:5]}...")

    embedding3 = embed_log_message(message3)
    print(f'\n--- Embedding for "{embedding3.original_message}" ---')
    print(f"Embedding vector (first 5 elements): {embedding3.embedding_vector[:5]}...")
