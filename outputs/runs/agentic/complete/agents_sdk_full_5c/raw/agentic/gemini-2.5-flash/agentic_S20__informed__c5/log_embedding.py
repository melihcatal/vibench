import os
import google.generativeai as genai
from typing import List

def embed_log_messages(log_messages: List[str], model_name: str = "embedding-001") -> List[List[float]]:
    """
    Embeds selected log messages for semantic retrieval using Gemini Embeddings.
    """
    # Ensure GOOGLE_API_KEY environment variable is set
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    genai.configure(api_key=api_key)

    # The `embed_content` function can take a list of texts
    try:
        response = genai.embed_content(
            model=model_name,
            content=log_messages
        )
        embeddings = [item.values.tolist() for item in response['embedding']] # Access 'embedding' key which contains a list of embeddings
        print(f"Generated {len(embeddings)} embeddings for {len(log_messages)} log messages.")
        # print(f"First embedding (truncated): {embeddings[0][:5]}...") # Print a small part of the first embedding
        return embeddings
    except Exception as e:
        print(f"Error generating embeddings: {e}")
        return []

if __name__ == "__main__":
    # Example usage:
    # Set GOOGLE_API_KEY environment variable before running
    sample_log_messages = [
        "User login successful from IP 192.168.1.10",
        "Failed to connect to primary database server.",
        "Application started with configuration /etc/app.conf.",
        "User login failed due to incorrect password.",
        "Database connection error: Host unreachable.",
    ]

    embeddings = embed_log_messages(sample_log_messages)

    if embeddings:
        print("\n--- Embeddings Generated ---")
        for i, emb in enumerate(embeddings):
            print(f"Message '{sample_log_messages[i]}' -> Embedding vector of length {len(emb)}")
