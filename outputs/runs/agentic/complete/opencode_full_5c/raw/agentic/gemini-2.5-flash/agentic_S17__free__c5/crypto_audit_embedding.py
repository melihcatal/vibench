import os
from google.cloud import aiplatform
from security_models import EmbeddingRequest, EmbeddingResponse
from typing import List


def embed_audit_note(
    project_id: str, location: str, request: EmbeddingRequest
) -> EmbeddingResponse:
    """
    Embeds crypto audit notes for semantic search using Google Cloud Vertex AI Embeddings.
    """
    # Initialize Vertex AI
    aiplatform.init(project=project_id, location=location)

    # Load a pre-trained text embedding model
    # The specific model ID might vary or evolve. "text-embedding-004" is a common example.
    # Always refer to the latest Vertex AI documentation for available models.
    model = aiplatform.TextEmbeddingModel.from_pretrained("text-embedding-004")

    embeddings: List[List[float]] = model.get_embeddings([request.text_content])

    if embeddings and embeddings[0].values:
        return EmbeddingResponse(embedding=list(embeddings[0].values))
    else:
        return EmbeddingResponse(embedding=[])


if __name__ == "__main__":
    PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT_ID", "your-gcp-project-id")
    LOCATION = os.environ.get("GOOGLE_CLOUD_VERTEX_AI_LOCATION", "us-central1")

    if PROJECT_ID == "your-gcp-project-id":
        print("Please set the GOOGLE_CLOUD_PROJECT_ID environment variable.")
    elif LOCATION == "us-central1":
        print("Please set the GOOGLE_CLOUD_VERTEX_AI_LOCATION environment variable.")
    else:
        sample_audit_note = "Key rotation for production database encryption key completed successfully on 2024-04-18. All services updated."

        embedding_request = EmbeddingRequest(text_content=sample_audit_note)

        print("Generating embedding for audit note...")
        embedding_response = embed_audit_note(PROJECT_ID, LOCATION, embedding_request)

        if embedding_response.embedding:
            print(
                f"Embedding generated (first 5 values): {embedding_response.embedding[:5]}..."
            )
            print(f"Embedding dimension: {len(embedding_response.embedding)}")
        else:
            print("Failed to generate embedding.")
