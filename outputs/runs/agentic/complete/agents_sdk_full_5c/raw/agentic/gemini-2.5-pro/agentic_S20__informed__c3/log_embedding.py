"""
Embeds log messages for semantic retrieval using Cohere.
"""
import os
import cohere
from typing import List

def embed_log_messages(log_messages: List[str]):
    """
    Generates embeddings for a list of log messages using Cohere.

    Requires the COHERE_API_KEY environment variable.
    """
    api_key = os.environ.get("COHERE_API_KEY")
    if not api_key:
        print("Error: COHERE_API_KEY environment variable is not set.")
        return None

    co = cohere.Client(api_key)

    try:
        response = co.embed(
            texts=log_messages,
            model="embed-english-v3.0",
            input_type="search_document",
            truncate="END"
        )
        return response.embeddings
    except cohere.CohereError as e:
        print(f"An error occurred with the Cohere API: {e}")
        return None

if __name__ == "__main__":
    logs_to_embed = [
        "User authentication failed: invalid password.",
        "Database connection timeout on host db-prod-1.",
        "Payment processing successful for order #98765.",
        "API rate limit exceeded for IP 192.168.1.100.",
        "User login failed due to wrong credentials provided.",
        "DB server is not responding."
    ]

    embeddings = embed_log_messages(logs_to_embed)

    if embeddings:
        print(f"Successfully generated {len(embeddings)} embeddings.")
        print("Dimension of the first embedding:", len(embeddings[0]))
        # print("First embedding (truncated):", embeddings[0][:5])
    else:
        print("Failed to generate embeddings.")
