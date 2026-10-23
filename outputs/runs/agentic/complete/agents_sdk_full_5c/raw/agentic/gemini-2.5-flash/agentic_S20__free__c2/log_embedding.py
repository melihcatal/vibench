import os
import vertexai
from vertexai.preview.language_models import TextEmbeddingModel
from observability_models import LogEmbeddingRequest, LogEmbeddingResponse

def embed_log_messages(request: LogEmbeddingRequest) -> LogEmbeddingResponse:
    """Embeds selected log messages for semantic retrieval using Vertex AI's PaLM 2 for Text Embedding."""
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    location = os.getenv("GCP_REGION", "us-central1") # Choose an appropriate region for Vertex AI

    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    vertexai.init(project=project_id, location=location)
    model = TextEmbeddingModel.from_pretrained("textembedding-gecko") # Or other suitable embedding model

    try:
        embeddings = model.get_embeddings(request.log_messages)
        vector_embeddings = [embedding.values for embedding in embeddings]
        
        return LogEmbeddingResponse(embeddings=vector_embeddings)

    except Exception as e:
        print(f"Error generating log embeddings: {e}")
        return LogEmbeddingResponse(embeddings=[])

if __name__ == "__main__":
    # Example usage
    log_messages_to_embed = [
        "User login successful from IP 192.168.1.10.",
        "Failed database connection to primary replica.",
        "New user registration completed: alice@example.com",
        "Error accessing database: connection refused.",
        "Successfully logged in from new device."
    ]

    request = LogEmbeddingRequest(log_messages=log_messages_to_embed)

    try:
        response = embed_log_messages(request)
        print(f"Generated {len(response.embeddings)} embeddings.")
        if response.embeddings:
            print(f"First embedding (truncated): {response.embeddings[0][:5]}...") # Print first 5 dimensions
            print(f"Embedding dimension: {len(response.embeddings[0])}")
            # In a real scenario, you'd store these embeddings in a vector database
            # and use them for semantic search or anomaly detection.
    except ValueError as e:
        print(f"Error: {e}")
        print("Please ensure GOOGLE_CLOUD_PROJECT and GCP_REGION environment variables are set.")
