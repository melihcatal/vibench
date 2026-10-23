from google.cloud import aiplatform
import os

def embed_transcript_segments(project_id: str, region: str, text_segments: list[str], model_name: str = "text-embedding-gecko@001"):
    """
    Embeds transcript segments for semantic retrieval using a Google Cloud Vertex AI embedding model.

    Args:
        project_id: Your Google Cloud project ID.
        region: The Google Cloud region where your Vertex AI model is deployed (e.g., "us-central1").
        text_segments: A list of text strings (segments) to embed.
        model_name: The name of the embedding model to use (e.g., "text-embedding-gecko@001").

    Returns:
        A list of embedding vectors, where each vector corresponds to a text segment.
    """
    aiplatform.init(project=project_id, location=region)
    # Using a predefined model for text embeddings
    model = aiplatform.language_models.TextEmbeddingModel.from_pretrained(model_name)

    embeddings = model.get_embeddings(text_segments)

    embedding_vectors = [embedding.values for embedding in embeddings]
    print(f"Generated embeddings for {len(text_segments)} segments using Vertex AI model: {model_name}.")
    return embedding_vectors
