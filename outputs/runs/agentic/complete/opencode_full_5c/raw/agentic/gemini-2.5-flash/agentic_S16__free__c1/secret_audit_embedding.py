import os
from typing import List
import vertexai
from vertexai.language_models import TextEmbeddingModel


def embed_audit_notes(audit_notes: List[str]) -> List[List[float]]:
    # Google Cloud Vertex AI provider identification
    # Ensure GOOGLE_CLOUD_PROJECT and GOOGLE_CLOUD_LOCATION (e.g., us-central1) are set
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")

    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    vertexai.init(project=project_id, location=location)
    model = TextEmbeddingModel.from_pretrained(
        "text-embedding-004"
    )  # Concrete model identifier

    embeddings = []
    for note in audit_notes:
        response = model.get_embeddings([note])
        if response and response[0].values:
            embeddings.append(response[0].values)
        else:
            embeddings.append([])  # Append empty list if embedding fails
    return embeddings


if __name__ == "__main__":
    # Example usage
    # Ensure GOOGLE_CLOUD_PROJECT and GOOGLE_CLOUD_LOCATION are set in your environment
    sample_notes = [
        "Secret 'db-password' rotated due to policy violation.",
        "Access to 'api-key-prod' granted to new service account.",
        "Review of 'ssh-key-internal' completed, no issues found.",
    ]

    try:
        print("Generating embeddings for audit notes...")
        note_embeddings = embed_audit_notes(sample_notes)
        for i, embedding in enumerate(note_embeddings):
            print(f"Note {i + 1} embedding (first 5 values): {embedding[:5]}...")
    except Exception as e:
        print(f"An error occurred during embedding generation: {e}")
