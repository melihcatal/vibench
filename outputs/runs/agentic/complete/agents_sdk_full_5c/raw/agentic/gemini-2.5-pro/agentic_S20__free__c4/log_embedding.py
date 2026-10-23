import os
import cohere
from typing import List

def get_log_embeddings(log_messages: List[str]) -> List[List[float]]:
    """
    Generates embeddings for a list of log messages using the Cohere API.

    Args:
        log_messages: A list of log message strings.

    Returns:
        A list of embedding vectors.
    """
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set.")
    
    co = cohere.Client(api_key)

    try:
        response = co.embed(
            texts=log_messages,
            model='embed-english-v3.0',
            input_type='search_document'
        )
        return response.embeddings
    except cohere.CohereError as e:
        print(f"Error calling Cohere API: {e}")
        return []

if __name__ == '__main__':
    # Log messages selected for semantic analysis or clustering
    logs_to_embed = [
        "User failed to log in: invalid credentials provided.",
        "Authentication error: password does not match for user 'admin'.",
        "Database connection timeout on write operation.",
        "Network error: could not resolve host 'db-primary'.",
        "Payment processing failed: card declined.",
        "User credit card was rejected by the payment gateway."
    ]

    embeddings = get_log_embeddings(logs_to_embed)

    if embeddings:
        print(f"Successfully generated {len(embeddings)} embeddings.")
        print("Embedding dimensions for the first log message:", len(embeddings[0]))
        # In a real application, you would store these vectors for similarity search.
        # For example, to find semantically similar log messages.
    else:
        print("Failed to generate embeddings.")
