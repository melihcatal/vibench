from google.cloud import aiplatform
from vertexai.language_models import TextEmbeddingModel
import os
from typing import List

def embed_transcript_segments(segments: List[str], project_id: str, location: str = "us-central1") -> List[List[float]]:
    """Embeds transcript segments for semantic retrieval using Vertex AI's textembedding-gecko model.

    Args:
        segments: A list of text segments (strings) from the transcript.
        project_id: Your Google Cloud project ID.
        location: The Google Cloud region where the Vertex AI model is hosted.

    Returns:
        A list of embedding vectors, where each vector is a list of floats.
    """
    aiplatform.init(project=project_id, location=location)
    model = TextEmbeddingModel.from_pretrained("textembedding-gecko") # Model family identifier

    embeddings = model.get_embeddings(segments)
    embedding_vectors = [embedding.values for embedding in embeddings]

    print(f"Generated {len(embedding_vectors)} embeddings. First embedding dimensions: {len(embedding_vectors[0])}")
    return embedding_vectors

if __name__ == '__main__':
    # Example usage
    PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "your-gcp-project-id")
    transcript_segments = [
        "The quick brown fox jumps over the lazy dog.",
        "Artificial intelligence is transforming many industries.",
        "The team discussed the project's timeline and budget constraints.",
        "How to train your dragon is a popular animated movie series."
    ]

    if PROJECT_ID == "your-gcp-project-id":
        print("Please set the GOOGLE_CLOUD_PROJECT environment variable or replace 'your-gcp-project-id' with your actual project ID.")
    else:
        print("Generating embeddings for transcript segments...")
        embeddings = embed_transcript_segments(transcript_segments, PROJECT_ID)
        for i, emb in enumerate(embeddings):
            print(f"Segment {i+1} embedding (first 5 values): {emb[:5]}...")
