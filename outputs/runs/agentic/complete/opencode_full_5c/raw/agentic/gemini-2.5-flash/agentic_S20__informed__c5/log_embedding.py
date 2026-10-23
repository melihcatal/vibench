from observability_client import get_embedding_model
from typing import List


def embed_log_messages(log_messages: List[str]) -> List[List[float]]:
    """Embeds selected log messages for semantic retrieval using the Gemini API (embedding model)."""
    model = get_embedding_model()

    if not log_messages:
        return []

    print(f"Generating embeddings for {len(log_messages)} log messages...")
    try:
        # The generate_embeddings method can take a list of texts
        response = model.embed_content(log_messages)

        embeddings = []
        if response and response.embeddings:
            for embedding_obj in response.embeddings:
                embeddings.append(embedding_obj.values)
            print("Embeddings generated successfully.")
            return embeddings
        else:
            print("Failed to generate embeddings: No embeddings found in response.")
            return []
    except Exception as e:
        print(f"Error generating embeddings: {e}")
        return []


if __name__ == "__main__":
    # Example usage:
    messages_to_embed = [
        "User login successful from IP 192.168.1.10",
        "Failed authentication attempt for user 'admin'",
        "Database connection error: timeout",
        "Cache write operation completed successfully for key 'products'",
        "Application started on port 8080",
        "User logout initiated from device mobile_app",
    ]

    embeddings = embed_log_messages(messages_to_embed)

    if embeddings:
        print("\n--- Generated Embeddings (first 2) ---")
        for i, emb in enumerate(embeddings):
            if i >= 2:
                break
            print(f"Message: {messages_to_embed[i][:50]}...")
            print(f"Embedding (first 5 values): {emb[:5]}...")
        print(f"Total embeddings generated: {len(embeddings)}")
        print(f"Dimension of embeddings: {len(embeddings[0]) if embeddings else 0}")
    else:
        print("No embeddings were generated.")
