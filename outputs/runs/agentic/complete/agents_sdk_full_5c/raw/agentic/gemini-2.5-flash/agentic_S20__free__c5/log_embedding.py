import os
from typing import List, Dict
import vertexai
from vertexai.language_models import TextEmbeddingModel

PROJECT_ID = os.environ.get("GCP_PROJECT_ID", "your-gcp-project-id")
LOCATION = os.environ.get("GCP_LOCATION", "us-central1")

def embed_log_messages(log_messages: List[str]) -> Dict[str, List[float]]:
    """Embeds selected log messages for semantic retrieval using Google Cloud Generative AI.

    Args:
        log_messages: A list of log message strings to embed.

    Returns:
        A dictionary where keys are original log messages and values are their embedding vectors.
    """
    vertexai.init(project=PROJECT_ID, location=LOCATION)

    # Use the appropriate embedding model
    # text-embedding-004 is a good general-purpose model
    model = TextEmbeddingModel.from_pretrained("text-embedding-004") 

    if not log_messages:
        return {}

    embeddings_map = {}
    try:
        # The `TextEmbeddingModel` can embed a batch of texts.
        # The embeddings are returned in the same order as the input texts.
        embeddings = model.get_embeddings(log_messages)
        for i, message in enumerate(log_messages):
            # Each embedding object has a `values` attribute which is the list of floats
            embeddings_map[message] = embeddings[i].values
    except Exception as e:
        print(f"Error during embedding: {e}")
        for msg in log_messages:
            embeddings_map[msg] = [] # Return empty list on error

    return embeddings_map

if __name__ == '__main__':
    # Example usage
    sample_log_messages = [
        "Database connection lost, attempting to reconnect.",
        "Failed to authenticate user due to invalid password.",
        "Successfully connected to the PostgreSQL database.",
        "User authentication failed, please check credentials.",
        "Network connectivity issue detected, retrying."
    ]

    log_embeddings = embed_log_messages(sample_log_messages)
    print("\n--- Log Message Embeddings ---")
    for original_msg, embedding_vector in log_embeddings.items():
        print(f"Original: '{original_msg}'\nEmbedding (first 5 dims): {embedding_vector[:5]}... (dim: {len(embedding_vector)})\n")

    # You can then use these embeddings for semantic search or clustering.
