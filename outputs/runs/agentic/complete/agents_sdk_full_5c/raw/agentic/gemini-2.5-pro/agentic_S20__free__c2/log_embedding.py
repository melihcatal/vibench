import os
import openai
from typing import List

def get_log_embeddings(log_messages: List[str]) -> List[List[float]]:
    """
    Generates embeddings for a list of log messages using OpenAI's API.

    Args:
        log_messages: A list of log message strings.

    Returns:
        A list of embedding vectors.
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set.")

    try:
        client = openai.OpenAI(api_key=api_key)
        response = client.embeddings.create(
            input=log_messages,
            # A specific, cost-effective, and performant model for embeddings
            model="text-embedding-3-small"
        )
        return [embedding.embedding for embedding in response.data]
    except openai.APIError as e:
        print(f"Error from OpenAI API: {e}")
        return []
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []

if __name__ == "__main__":
    logs_to_embed = [
        "Authentication successful for user_id: 12345",
        "User 12345 logged in.",
        "Failed to connect to database: Connection refused.",
        "Database connection timeout on host db.prod.internal.",
        "User 54321 updated their profile picture.",
        "Profile update for user_id 54321 successful.",
    ]

    print(f"Generating embeddings for {len(logs_to_embed)} log messages...")
    try:
        embeddings = get_log_embeddings(logs_to_embed)
        if embeddings:
            print(f"Successfully generated {len(embeddings)} embeddings.")
            for i, emb in enumerate(embeddings):
                # Print the first few dimensions of each embedding for verification
                print(f"Log {i+1}: {logs_to_embed[i][:40]}... -> Embedding dims: {len(emb)}, "
                      f"First 3: {emb[:3]}")
    except ValueError as e:
        print(e)
