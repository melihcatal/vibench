import os
import cohere
from typing import List


def embed_log_messages(log_messages: List[str]) -> List[List[float]]:
    """
    Generates embeddings for a list of log messages using Cohere.
    """
    api_key = os.environ.get("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set.")

    co = cohere.Client(api_key)

    if not log_messages:
        return []

    try:
        # Using a model optimized for retrieval
        response = co.embed(
            texts=log_messages, model="embed-english-v3.0", input_type="search_document"
        )
        return response.embeddings
    except cohere.CohereError as e:
        print(f"An error occurred with the Cohere API: {e}")
        return []


if __name__ == "__main__":
    # Example Usage:
    # Set COHERE_API_KEY environment variable
    logs = [
        "Authentication successful for user_id: 550e8400-e29b-41d4-a716-446655440000",
        "Failed login attempt for username: 'admin'",
        "Database connection established successfully.",
        "Error: Timeout while connecting to payment gateway.",
        "User profile updated for user_id: f47ac10b-58cc-4372-a567-0e02b2c3d479",
    ]

    embeddings = embed_log_messages(logs)

    if embeddings:
        print(f"Successfully generated {len(embeddings)} embeddings.")
        # Print the dimension of the first embedding as a sample
        print(f"Dimension of the first log embedding: {len(embeddings[0])}")
    else:
        print("Failed to generate embeddings.")
