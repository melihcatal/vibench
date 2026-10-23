import vertexai
from vertexai.language_models import TextEmbeddingInput, TextEmbeddingModel

def embed_caption_chunks(project_id: str, location: str, caption_chunks: list[str]) -> list[list[float]]:
    """
    Embeds caption chunks using Google Cloud's Vertex AI Text Embedding Model.

    Args:
        project_id: The Google Cloud project ID.
        location: The Google Cloud region (e.g., "us-central1").
        caption_chunks: A list of caption text chunks to embed.

    Returns:
        A list of embeddings, where each embedding is a list of floats.
    """
    vertexai.init(project=project_id, location=location)
    model = TextEmbeddingModel.from_pretrained("text-embedding-004")
    inputs = [TextEmbeddingInput(text_content=chunk, task_type="SEMANTIC_SIMILARITY") for chunk in caption_chunks]
    embeddings = model.get_embeddings(inputs)
    return [embedding.values for embedding in embeddings]
