import os
from google.cloud import aiplatform
from observability_models import EmbeddingRequest, EmbeddingResponse

def embed_log_message(
    request: EmbeddingRequest,
    project_id: str = None,
    location: str = "us-central1",
    model_name: str = "text-embedding-004"
) -> EmbeddingResponse:
    """Embeds selected log messages for semantic retrieval using Google Cloud Vertex AI Embeddings API."""

    if project_id is None:
        project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
        if not project_id:
            raise ValueError("project_id must be provided or GOOGLE_CLOUD_PROJECT env var set.")

    aiplatform.init(project=project_id, location=location)
    model = aiplatform.TextEmbeddingModel.from_pretrained(model_name)

    print(f"Generating embedding for log message with Vertex AI model {model_name}...")
    try:
        # The `embed` method takes a list of texts and returns a list of embedding objects.
        embeddings = model.embed(requests=[request.text])
        
        if embeddings and embeddings[0].values:
            return EmbeddingResponse(embedding=embeddings[0].values)
        else:
            raise ValueError("Failed to generate embedding: No embedding values returned.")

    except Exception as e:
        print(f"Error generating log message embedding: {e}")
        return EmbeddingResponse(
            embedding=[] # Return an empty list or raise an error based on desired behavior
        )

if __name__ == "__main__":
    # Example usage:
    # Set GOOGLE_CLOUD_PROJECT environment variable before running
    # export GOOGLE_CLOUD_PROJECT="your-gcp-project-id"
    # Ensure Vertex AI API is enabled and you have necessary permissions.
    
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if project_id:
        print("\n--- Embedding a log message ---")
        log_message1 = "User login failed due to incorrect password attempt for user_id: 456."
        request1 = EmbeddingRequest(text=log_message1)
        response1 = embed_log_message(request1, project_id=project_id)
        print(f"Original log: '{log_message1}'")
        print(f"Embedding (first 5 values): {response1.embedding[:5]}...")
        print(f"Embedding dimension: {len(response1.embedding)}")

        print("\n--- Embedding another log message with similar context ---")
        log_message2 = "Authentication error: Invalid credentials provided by user 456."
        request2 = EmbeddingRequest(text=log_message2)
        response2 = embed_log_message(request2, project_id=project_id)
        print(f"Original log: '{log_message2}'")
        print(f"Embedding (first 5 values): {response2.embedding[:5]}...")
        print(f"Embedding dimension: {len(response2.embedding)}")

        print("\n--- Embedding a different log message ---")
        log_message3 = "Database connection established successfully on port 5432."
        request3 = EmbeddingRequest(text=log_message3)
        response3 = embed_log_message(request3, project_id=project_id)
        print(f"Original log: '{log_message3}'")
        print(f"Embedding (first 5 values): {response3.embedding[:5]}...")
        print(f"Embedding dimension: {len(response3.embedding)}")

    else:
        print("Please set the GOOGLE_CLOUD_PROJECT environment variable.")
