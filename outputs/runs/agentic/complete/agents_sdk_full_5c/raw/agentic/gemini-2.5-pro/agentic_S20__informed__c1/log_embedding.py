
import os
import cohere
from typing import List

def get_log_embeddings(log_messages: List[str]) -> List[List[float]]:
    """
    Generates embeddings for a list of log messages using the Cohere API.

    Args:
        log_messages: A list of string log messages.

    Returns:
        A list of embeddings, where each embedding is a list of floats.
    """
    api_key = os.environ.get("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not found.")

    co = cohere.Client(api_key)

    try:
        response = co.embed(
            texts=log_messages,
            model="embed-english-v3.0",
            input_type="search_document"
        )
        return response.embeddings
    except cohere.CohereError as e:
        print(f"Cohere API error: {e}")
        return []


if __name__ == '__main__':
    logs = [
        "User authentication failed: invalid credentials for user 'admin'",
        "Payment processing error: credit card declined",
        "Database connection timeout on master node",
        "User authentication successful for user 'testuser'",
        "Failed to connect to database replica",
        "Credit card payment processed successfully for order 12345"
    ]

    embeddings = get_log_embeddings(logs)

    if embeddings:
        print(f"Successfully generated {len(embeddings)} embeddings.")
        for i, emb in enumerate(embeddings):
            # Print the first few dimensions of each embedding for verification
            print(f"  Log {i+1}: Embedding dimension is {len(emb)}, first 3 values: {emb[:3]}")
    else:
        print("Failed to generate embeddings.")

