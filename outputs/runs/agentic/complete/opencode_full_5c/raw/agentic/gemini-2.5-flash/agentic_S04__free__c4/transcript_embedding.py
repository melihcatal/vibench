from google.cloud import aiplatform
from typing import List


def embed_transcript_segments(
    segments: List[str], project_id: str, location: str
) -> List[List[float]]:
    """
    Generates embeddings for a list of transcript segments using Google Cloud Vertex AI (text-embedding-004).
    """
    aiplatform.init(project=project_id, location=location)

    # Use the text embedding model
    # The specific model ID might vary, "text-embedding-004" is a common choice for embeddings.
    model = aiplatform.LanguageModel.from_pretrained("text-embedding-004")

    # Generate embeddings for each segment
    embeddings = model.predict(segments)
    return embeddings.text_embeddings


if __name__ == "__main__":
    # Example usage
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # Replace with your Google Cloud Project ID and location
    project_id = "your-gcp-project-id"
    location = "us-central1"

    transcript_segments = [
        "The quick brown fox jumps over the lazy dog.",
        "A fast, ginger canine leaps above a sluggish hound.",
        "This sentence is about something completely different.",
        "The cat sat on the mat.",
    ]

    # embeddings = embed_transcript_segments(transcript_segments, project_id, location)
    # for i, embedding in enumerate(embeddings):
    #     print(f"Embedding for segment {i+1} (first 5 values): {embedding[:5]}...")
