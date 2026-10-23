from google.cloud import aiplatform
from typing import List

def platform_output_embedding(project_id: str, location: str, text: str) -> List[float]:
    """Embeds platform outputs for evaluation or retrieval using Google Vertex AI Embedding API.

    Args:
        project_id: The Google Cloud project ID.
        location: The Google Cloud region where the model is deployed.
        text: The text content to embed.

    Returns:
        A list of floats representing the embedding of the text.
    """
    aiplatform.init(project=project_id, location=location)
    # The embedding model name often follows a pattern like 'text-embedding-gecko@001'
    model = aiplatform.TextEmbeddingModel.from_pretrained("text-embedding-gecko@001")
    embeddings = model.get_embeddings([text])
    return embeddings[0].values
