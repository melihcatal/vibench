import os
import cohere
from typing import List


def get_log_embeddings(log_messages: List[str]) -> List[List[float]]:
    """
    Generates embeddings for a list of log messages using the Cohere API.
    """
    api_key = os.environ.get("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set.")

    co = cohere.Client(api_key)

    try:
        response = co.embed(
            texts=log_messages, model="embed-english-v3.0", input_type="search_document"
        )
        return response.embeddings
    except cohere.CohereError as e:
        print(f"An error occurred with the Cohere API: {e}")
        return []


if __name__ == "__main__":
    logs_for_embedding = [
        "User authentication failed: invalid password",
        "Successful user login for customer_id 12345",
        "Database connection timeout error",
        "Payment processing failed: insufficient funds",
        "Payment transaction completed successfully",
        "Network error: Unable to reach upstream service",
    ]

    try:
        embeddings = get_log_embeddings(logs_for_embedding)
        if embeddings:
            print(f"Successfully generated {len(embeddings)} embeddings.")
            for i, emb in enumerate(embeddings):
                # Print the first few dimensions of each embedding as a sample
                print(
                    f"  Log {i + 1}: Embedding dimension is {len(emb)}, "
                    f"starts with {emb[:3]}"
                )
    except ValueError as e:
        print(e)
