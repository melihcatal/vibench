import os
from typing import Dict, List
from openai import OpenAI


def embed_asset_metadata_and_text(
    metadata: Dict[str, str],
    extracted_text: str,
    model: str = "text-embedding-3-small",
) -> Dict[str, List[float]]:
    """
    Embeds object metadata and extracted text using OpenAI's embeddings API.

    Args:
        metadata: Dictionary of object metadata.
        extracted_text: Text extracted from the object.
        model: OpenAI embeddings model identifier (e.g., "text-embedding-3-small").

    Returns:
        Dictionary containing embeddings for metadata and text.

    Raises:
        Exception: If the embedding process fails.
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    try:
        # Combine metadata and text for embedding
        combined_text = " ".join([f"{k}: {v}" for k, v in metadata.items()])
        combined_text += f" Text: {extracted_text}"

        response = client.embeddings.create(
            input=combined_text,
            model=model,
        )

        return {
            "embedding": response.data[0].embedding,
            "model": model,
        }
    except Exception as e:
        raise Exception(f"Failed to generate embeddings: {e}")
