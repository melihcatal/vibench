import os
import cohere
from typing import List

def get_log_embeddings(log_messages: List[str]) -> list:
    """
    Generates embeddings for a list of log messages using the Cohere API.

    Embeddings can be used for semantic search, clustering, or anomaly
    detection on logs, allowing you to find similar logs based on meaning
    rather than just keywords.

    Args:
        log_messages: A list of strings, where each string is a log message.

    Returns:
        A list of embedding vectors.
    """
    api_key = os.environ.get("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set.")
    
    co = cohere.Client(api_key)

    if not log_messages:
        return []

    try:
        # Using a modern, high-performance model for English embeddings.
        response = co.embed(
            texts=log_messages,
            model="embed-english-v3.0",
            input_type="search_document"
        )
        return response.embeddings
    except cohere.errors.CohereError as e:
        print(f"An error occurred with the Cohere API: {e}")
        return []

# Example usage:
# logs_to_embed = [
#     "User authentication failed: invalid credentials",
#     "Failed to connect to database: timeout",
#     "User password not strong enough",
#     "Database connection timed out during query",
#     "Successful user login for user 'admin'",
# ]
#
# embeddings = get_log_embeddings(logs_to_embed)
# if embeddings:
#     print(f"Successfully generated {len(embeddings)} embeddings.")
#     print(f"Dimension of first embedding: {len(embeddings[0])}")
