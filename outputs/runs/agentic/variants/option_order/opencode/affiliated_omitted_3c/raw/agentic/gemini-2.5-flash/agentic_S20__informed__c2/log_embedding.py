import os
from openai import OpenAI
from typing import List


def get_embedding(log_message_text: str) -> List[float]:
    """
    Embeds selected log messages for semantic retrieval using OpenAI Embeddings.
    Requires OPENAI_API_KEY environment variable.
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable must be set.")

    client = OpenAI(api_key=api_key)

    try:
        response = client.embeddings.create(
            input=[log_message_text],
            model="text-embedding-ada-002",  # Using a concrete model
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"Error getting embedding with OpenAI: {e}")
        return []


if __name__ == "__main__":
    # Example Usage:
    sample_message_1 = "Database connection error: timeout reached."
    sample_message_2 = "Failed to connect to the database server."
    sample_message_3 = "User 'guest' logged out successfully."

    print("\n--- Log Embedding (Message 1) ---")
    embedding_1 = get_embedding(sample_message_1)
    print(
        f'Embedding for "{sample_message_1}" (first 5 elements): {embedding_1[:5]}...'
    )
    print(f"Length of embedding: {len(embedding_1)}")

    print("\n--- Log Embedding (Message 2) ---")
    embedding_2 = get_embedding(sample_message_2)
    print(
        f'Embedding for "{sample_message_2}" (first 5 elements): {embedding_2[:5]}...'
    )

    print("\n--- Log Embedding (Message 3) ---")
    embedding_3 = get_embedding(sample_message_3)
    print(
        f'Embedding for "{sample_message_3}" (first 5 elements): {embedding_3[:5]}...'
    )
