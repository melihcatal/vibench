import os
import google.generativeai as genai
from typing import List


def embed_log_messages(messages: List[str]) -> List[List[float]]:
    """Embeds selected log messages for semantic retrieval using Google Gemini Embeddings."""
    google_api_key = os.environ.get("GOOGLE_API_KEY")
    if not google_api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=google_api_key)

    try:
        # The embedding model for text
        model = "models/embedding-001"

        # Generate embeddings in batches if many messages
        embeddings = []
        for message in messages:
            response = genai.embed_content(
                model=model, content=message, task_type="SEMANTIC_SIMILARITY"
            )
            embeddings.append(response["embedding"])

        return embeddings
    except Exception as e:
        print(f"Error generating embeddings with Gemini API: {e}")
        return []


if __name__ == "__main__":
    # Example usage:
    log_messages = [
        "Database connection error: timeout",
        "Failed to establish connection to primary database server",
        "User login attempt failed due to invalid credentials",
        "Authentication failed for user 'john.doe'",
        "High memory usage detected on server host-prod-1",
        "Memory leak in process xyz",
    ]

    print("\n--- Log Message Embeddings ---")
    message_embeddings = embed_log_messages(log_messages)

    if message_embeddings:
        for i, embedding in enumerate(message_embeddings):
            print(
                f"Message '{log_messages[i]}' embedding (first 5 dims): {embedding[:5]}..."
            )
            print(f"Embedding dimension: {len(embedding)}")
    else:
        print("Failed to generate embeddings.")
