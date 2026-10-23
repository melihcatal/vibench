import os
from google.cloud import aiplatform
from typing import List

def get_text_embedding(log_messages: List[str]) -> List[List[float]]:
    """
    Embeds a list of log messages using Google Cloud's Vertex AI.

    Args:
        log_messages: A list of log messages to embed.

    Returns:
        A list of embeddings, where each embedding is a list of floats.
    """
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    # Initialize Vertex AI
    aiplatform.init(project=project_id, location="us-central1") # Or your preferred region

    # Choose an embedding model
    model = aiplatform.models.TextEmbeddingModel.from_pretrained("text-embedding-004")

    # Get embeddings
    embeddings = model.embed_text(log_messages)

    return [embedding.values for embedding in embeddings]

if __name__ == "__main__":
    # Example usage:
    messages_to_embed = [
        "User login failed for user_id: 123 due to incorrect password.",
        "Database connection established successfully.",
        "Error: File not found in path /var/log/app.log",
        "Successful API call to /api/v1/data endpoint.",
    ]

    try:
        log_embeddings = get_text_embedding(messages_to_embed)
        for i, embedding in enumerate(log_embeddings):
            print(f"Embedding for message '{messages_to_embed[i]}': {embedding[:5]}...") # Print first 5 dimensions
    except ValueError as e:
        print(f"Error: {e}")
        print("Please set the GOOGLE_CLOUD_PROJECT environment variable.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
