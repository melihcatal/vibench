import os
import google.generativeai as genai
from typing import List


def embed_log_messages_gemini(log_messages: List[str]) -> List[List[float]]:
    """Embeds selected log messages for semantic retrieval using Gemini Embeddings."""
    # Ensure GOOGLE_API_KEY environment variable is set
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

    # The embedding model is 'embedding-001'
    model_name = "embedding-001"

    if not log_messages:
        return []

    embeddings = []
    for message in log_messages:
        try:
            # The task_type for logging might be semantic_similarity or retrieval_query/document
            # For general log message embedding, semantic_similarity is a good default.
            response = genai.embed_content(
                model=model_name,
                content=message,
                task_type="RETRIEVAL_DOCUMENT",  # or SEMANTIC_SIMILARITY
            )
            embeddings.append(response["embedding"])
        except Exception as e:
            print(f"Error embedding message ''{message}'': {e}")
            embeddings.append([])  # Append an empty list or handle error as appropriate

    return embeddings


if __name__ == "__main__":
    # Example usage: Ensure GOOGLE_API_KEY environment variable is set
    messages_to_embed = [
        "Database connection error: Too many connections",
        "Failed to connect to primary database replica",
        "User authentication failed for jdoe",
        "Incorrect password provided for user jdoe",
        "Application started successfully on port 8080",
        "Server is listening on HTTP port 8080",
    ]

    print("Generating embeddings for log messages...")
    log_embeddings = embed_log_messages_gemini(messages_to_embed)

    if log_embeddings:
        print(f"Generated {len(log_embeddings)} embeddings.")
        for i, embedding in enumerate(log_embeddings):
            print(
                f"Message '{messages_to_embed[i]}' embedding (first 5 values): {embedding[:5]}..."
            )
    else:
        print("No embeddings were generated.")
