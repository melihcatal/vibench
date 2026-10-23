import vertexai
from vertexai.language_models import TextEmbeddingModel
import os

def initialize_vertex_ai(project_id: str, location: str):
    """Initializes Vertex AI with the given project ID and location.
    This should be called once before making embedding calls.
    """
    vertexai.init(project=project_id, location=location)


def get_embedding_model():
    """Returns a Google Cloud Vertex AI TextEmbeddingModel client.
    Using text-embedding-004 as an example model_id.
    """
    # 'text-embedding-004' is a common and versatile model.
    # Other models like 'text-multilingual-embedding-002' might be suitable for multilingual data.
    return TextEmbeddingModel.from_pretrained("text-embedding-004")


def embed_text_segment(text: str, project_id: str, location: str = 'us-central1') -> list[float]:
    """Embeds a single text segment using Google Cloud Vertex AI Embeddings.

    Args:
        text: The text content to embed.
        project_id: Your Google Cloud project ID.
        location: The Vertex AI location (e.g., 'us-central1').

    Returns:
        A list of floats representing the embedding vector.
    """
    # Ensure Vertex AI is initialized (can be done once at application startup)
    # initialize_vertex_ai(project_id, location)

    model = get_embedding_model()
    try:
        embeddings = model.get_embeddings([text])
        if embeddings and embeddings[0].values:
            return embeddings[0].values
        return []
    except Exception as e:
        print(f"Error embedding text: {e}")
        return []

def embed_transcript_segments(segments: list[str], project_id: str, location: str = 'us-central1') -> list[list[float]]:
    """Embeds multiple transcript segments using Google Cloud Vertex AI Embeddings.

    Args:
        segments: A list of text segments to embed.
        project_id: Your Google Cloud project ID.
        location: The Vertex AI location (e.g., 'us-central1').

    Returns:
        A list of embedding vectors, one for each segment.
    """
    # Ensure Vertex AI is initialized (can be done once at application startup)
    # initialize_vertex_ai(project_id, location)

    model = get_embedding_model()
    try:
        embeddings = model.get_embeddings(segments)
        return [embedding.values for embedding in embeddings if embedding.values]
    except Exception as e:
        print(f"Error embedding segments: {e}")
        return []

# Example usage
# if __name__ == "__main__":
#     # project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
#     # if not project_id:
#     #     raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")
#     # 
#     # initialize_vertex_ai(project_id, 'us-central1') # Initialize once
#     # 
#     # sample_segments = [
#     #     "The quick brown fox jumps over the lazy dog.",
#     #     "A canine is resting while a fox leaps above it.",
#     #     "The capital of France is Paris."
#     # ]
#     # 
#     # embedded_segments = embed_transcript_segments(sample_segments, project_id)
#     # for i, embedding in enumerate(embedded_segments):
#     #     print(f"Segment {i+1} embedding (first 5 dims): {embedding[:5]}...")
#     pass
