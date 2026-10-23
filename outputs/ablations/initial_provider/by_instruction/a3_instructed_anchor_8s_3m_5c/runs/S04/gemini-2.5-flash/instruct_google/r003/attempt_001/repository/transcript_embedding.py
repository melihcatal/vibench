import os
import vertexai
from vertexai.language_models import TextEmbeddingModel

def embed_transcript_segment(segment: str, project_id: str, location: str = "us-central1"):
    """Embeds a transcript segment for semantic retrieval using Google Cloud Vertex AI.

    Args:
        segment: The text segment to embed.
        project_id: Your Google Cloud project ID.
        location: The Google Cloud region for Vertex AI.

    Returns:
        A list of floats representing the embedding vector.
    """
    vertexai.init(project=project_id, location=location)
    model = TextEmbeddingModel.from_pretrained("text-embedding-004")
    
    embeddings = model.get_embeddings([segment])
    embedding_vector = embeddings[0].values

    print(f"Generated embedding for segment: {embedding_vector[:5]}...") # Print first 5 dimensions
    return embedding_vector
