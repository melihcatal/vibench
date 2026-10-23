import os
import cohere
from typing import List

def get_log_embeddings(log_messages: List[str]) -> List[List[float]]:
    """
    Generates embeddings for a list of log messages using the Cohere API.

    Args:
        log_messages: A list of strings, where each string is a log message.

    Returns:
        A list of embeddings, where each embedding is a list of floats.
    """
    api_key = os.environ.get("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set.")

    co = cohere.Client(api_key)

    try:
        # Using a model optimized for retrieval and semantic search
        response = co.embed(
            texts=log_messages,
            model="embed-english-v3.0",
            input_type="search_document"
        )
        return response.embeddings
    except cohere.CohereError as e:
        print(f"An error occurred with the Cohere API: {e}")
        return []

if __name__ == '__main__':
    # Example log messages for which we want to find semantically similar entries
    logs_to_embed = [
        "User failed to log in: incorrect password.",
        "Authentication error for user 'admin': invalid credentials.",
        "Database connection timed out after 3 retries.",
        "Payment processing failed for order #12345.",
        "Could not connect to the primary database server.",
        "Credit card transaction declined by payment gateway.",
    ]

    embeddings = get_log_embeddings(logs_to_embed)

    if embeddings:
        print(f"Successfully generated {len(embeddings)} embeddings.")
        # Print the dimension of the first embedding as a sample
        print(f"Dimension of the first embedding: {len(embeddings[0])}")
        # print(f"First embedding vector (first 5 dimensions): {embeddings[0][:5]}")
    else:
        print("Failed to generate embeddings.")
