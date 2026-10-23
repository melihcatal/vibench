import os
from typing import Dict, List

from google.cloud import aiplatform
from google.api_core.exceptions import GoogleAPIError


def asset_metadata_embedding(metadata: Dict[str, str], text: str = "") -> List[float]:
    """
    Embeds object metadata and extracted text for search using Google Cloud Vertex AI.

    Args:
        metadata: Dictionary of metadata key-value pairs.
        text: Optional extracted text from the asset.

    Returns:
        A list of floats representing the embedding vector.

    Raises:
        GoogleAPIError: If the embedding process fails.
    """
    aiplatform.init(
        project=os.getenv("GOOGLE_CLOUD_PROJECT"),
        location=os.getenv("GOOGLE_CLOUD_REGION"),
    )

    combined_input = " ".join([f"{k}:{v}" for k, v in metadata.items()])
    if text:
        combined_input += f" {text}"

    model = aiplatform.TextEmbeddingModel.from_pretrained("textembedding-gecko@latest")
    embeddings = model.get_embeddings([combined_input])

    return embeddings[0].values
