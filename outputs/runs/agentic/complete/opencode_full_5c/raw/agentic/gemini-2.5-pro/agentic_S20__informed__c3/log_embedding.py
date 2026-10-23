import os
import cohere
from typing import List


def embed_log_messages(log_messages: List[str]) -> List[List[float]]:
    """
    Embeds selected log messages for semantic retrieval using Cohere.
    """
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set.")

    co = cohere.Client(api_key)

    try:
        response = co.embed(
            texts=log_messages, model="embed-english-v3.0", input_type="search_document"
        )
        return response.embeddings
    except cohere.CohereError as e:
        print(f"Cohere API error: {e}")
        return []


if __name__ == "__main__":
    logs = [
        "Authentication error: invalid credentials provided for user 'admin'",
        "Database connection timeout on primary cluster",
        "User 'guest' logged in successfully from IP 192.168.1.10",
        "Failed to process payment: credit card declined",
        "Invalid token for user 'admin'. Please re-authenticate.",
    ]

    embeddings = embed_log_messages(logs)

    if embeddings:
        print(f"Successfully generated {len(embeddings)} embeddings.")
        print("Dimension of first embedding:", len(embeddings[0]))
        # print("First embedding (truncated):", embeddings[0][:5])
