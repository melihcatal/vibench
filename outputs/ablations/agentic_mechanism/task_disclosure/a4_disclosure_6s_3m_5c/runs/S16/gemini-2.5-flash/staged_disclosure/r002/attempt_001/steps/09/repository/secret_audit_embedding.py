import os
from google.cloud import aiplatform

def embed_text(texts: list[str]) -> list[list[float]]:
    """
    Embeds a list of texts using Google's Vertex AI TextEmbeddingModel.

    Args:
        texts: A list of strings to embed.

    Returns:
        A list of embeddings, where each embedding is a list of floats.
    """
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")

    aiplatform.init(project=project_id, location=location)

    # This is the identifiable part for the provider (Google Cloud Vertex AI)
    # and the specific model used for embeddings.
    model = aiplatform.TextEmbeddingModel.from_pretrained("text-embedding-004")
    embeddings = model.get_embeddings(texts)
    return [embedding.values for embedding in embeddings]

if __name__ == "__main__":
    # Example usage (requires GOOGLE_CLOUD_PROJECT and GOOGLE_CLOUD_LOCATION env vars)
    # and authentication to Google Cloud.
    audit_notes = [
        "Audit revealed unencrypted API keys in configuration files.",
        "Access logs show unauthorized attempts to access sensitive data.",
        "Multi-factor authentication is not enforced for all administrative accounts.",
        "Review of third-party integrations identified a potential data leakage risk.",
        "Employee offboarding process did not revoke all system access.",
    ]
    
    if os.environ.get("GOOGLE_CLOUD_PROJECT"):
        print("Generating embeddings for audit notes...")
        note_embeddings = embed_text(audit_notes)
        for i, embedding in enumerate(note_embeddings):
            print(f"Note {i+1} embedding (first 5 values): {embedding[:5]}...")
    else:
        print("Please set GOOGLE_CLOUD_PROJECT environment variable to run example.")
        print("Example: export GOOGLE_CLOUD_PROJECT="your-gcp-project-id"")
