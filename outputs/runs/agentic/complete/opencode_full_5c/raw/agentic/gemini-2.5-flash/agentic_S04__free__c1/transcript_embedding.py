import os
import vertexai
from vertexai.language_models import TextEmbeddingModel


def embed_transcript_segments(project_id: str, location: str, segments: list[str]):
    """Embeds transcript segments for semantic retrieval using Google Cloud Vertex AI's TextEmbeddingModel.

    Args:
        project_id: The Google Cloud project ID.
        location: The Google Cloud region (e.g., "us-central1").
        segments: A list of text segments to embed.

    Returns:
        A list of embedding vectors.
    """
    vertexai.init(project=project_id, location=location)
    model = TextEmbeddingModel.from_pretrained(
        "text-embedding-004"
    )  # Using a text embedding model

    embeddings = model.get_embeddings(segments)
    return [embedding.values for embedding in embeddings]


if __name__ == "__main__":
    # Example usage
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    location = "us-central1"  # Or your preferred Vertex AI region
    transcript_segments = [
        "The quick brown fox jumps over the lazy dog.",
        "A group of people are discussing financial results.",
        "Artificial intelligence is transforming many industries.",
    ]

    if project_id and location:
        print(f"Embedding {len(transcript_segments)} transcript segments...")
        segment_embeddings = embed_transcript_segments(
            project_id, location, transcript_segments
        )
        for i, embedding in enumerate(segment_embeddings):
            print(f"Embedding for segment {i + 1} (first 5 values): {embedding[:5]}...")
            print(f"Embedding dimension: {len(embedding)}")
            print("-" * 20)
    else:
        print(
            "GOOGLE_CLOUD_PROJECT or VERTEX_AI_LOCATION environment variable not set."
        )
