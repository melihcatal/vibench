import os
import google.generativeai as genai
from observability_client import observability_client

def embed_log_message(log_message: str) -> list[float]:
    """
    Embeds selected log messages for semantic retrieval using Gemini Embeddings.

    Args:
        log_message: The text of the log message to embed.

    Returns:
        A list of floats representing the embedding vector.
    """
    model_name = observability_client.get_gemini_embedding_model("models/embedding-001")

    try:
        response = genai.embed_content(
            model=model_name,
            content=log_message,
            task_type="RETRIEVAL_DOCUMENT" # or "RETRIEVAL_QUERY" depending on usage
        )
        embedding = response["embedding"]
        print(f"Successfully embedded log message (first 5 dims): {embedding[:5]}...")
        return embedding
    except Exception as e:
        print(f"Error embedding log message '{log_message}': {e}")
        return []

if __name__ == "__main__":
    # Example usage:
    # Ensure GOOGLE_API_KEY environment variable is set
    messages_to_embed = [
        "Database connection timed out.",
        "Failed to establish connection to the PostgreSQL database.",
        "User authentication failed due to invalid credentials.",
        "Login attempt with incorrect password."
    ]

    print("Generating embeddings for log messages...")
    for msg in messages_to_embed:
        print(f"\n--- Embedding Message: '{msg}' ---")
        embedding_vector = embed_log_message(msg)
        if embedding_vector:
            print(f"Embedding vector length: {len(embedding_vector)}")
        else:
            print("Failed to get embedding.")
