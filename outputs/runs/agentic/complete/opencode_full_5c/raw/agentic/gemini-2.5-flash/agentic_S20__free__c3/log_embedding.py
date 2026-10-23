import os
from typing import List, Dict, Any
from google.cloud import aiplatform
from vertexai.language_models import TextEmbeddingModel
from observability_models import EmbeddingRequest

# Ensure GOOGLE_CLOUD_PROJECT environment variable is set
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
if not PROJECT_ID:
    raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

# Initialize Vertex AI SDK
aiplatform.init(
    project=PROJECT_ID, location="us-central1"
)  # Choose an appropriate region


def embed_log_messages(request: EmbeddingRequest) -> List[Dict[str, Any]]:
    try:
        model = TextEmbeddingModel.from_pretrained(
            "text-embedding-004"
        )  # Using a suitable embedding model

        # Vertex AI embedding models have a limit on the number of texts per request (e.g., 20 or 250)
        # and a token limit per text (e.g., 512). Batching might be needed for very long lists or texts.
        embeddings = model.get_embeddings(request.text)

        results = []
        for i, embedding in enumerate(embeddings):
            results.append({"text": request.text[i], "embedding": embedding.values})

        return results

    except Exception as e:
        return [{"error": f"Error generating embeddings: {e}"}]


if __name__ == "__main__":
    # Example usage:
    messages_to_embed = [
        "User login event with IP 192.168.1.10",
        "Failed database connection, retrying...",
        "New session started for admin user.",
        "Error: NullPointerException in PaymentProcessor.java",
        "Database connection successful.",
    ]

    embedding_request = EmbeddingRequest(text=messages_to_embed)
    embeddings_result = embed_log_messages(embedding_request)

    print("\n--- Log Message Embeddings ---")
    if "error" in embeddings_result[0]:
        print(embeddings_result[0]["error"])
    else:
        for item in embeddings_result:
            print(f"Text: '{item['text']}'")
            print(f"Embedding (first 5 values): {item['embedding'][:5]}...")
            print(f"Embedding dimension: {len(item['embedding'])}")
            print("\n")
