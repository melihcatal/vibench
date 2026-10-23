import os
from typing import Dict, List

from sentence_transformers import SentenceTransformer


def embed_asset_metadata_and_text(
    metadata: Dict[str, str],
    extracted_text: str,
    model_name: str = "all-MiniLM-L6-v2",
) -> List[float]:
    """
    Embeds object metadata and extracted text for search using Sentence Transformers.

    Args:
        metadata: Dictionary containing object metadata.
        extracted_text: Text extracted from the stored asset.
        model_name: Sentence Transformer model identifier (e.g., 'all-MiniLM-L6-v2').

    Returns:
        List[float]: Embedding vector for the combined metadata and text.

    Raises:
        Exception: If embedding generation fails.
    """
    model = SentenceTransformer(model_name)

    combined_text = " ".join([f"{k}: {v}" for k, v in metadata.items()])
    combined_text += f" Text: {extracted_text}"

    embedding = model.encode(combined_text, convert_to_tensor=False)
    return embedding.tolist()
