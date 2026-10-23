from typing import Dict, List, Optional

import numpy as np
from sentence_transformers import SentenceTransformer
from botocore.exceptions import ClientError


def embed_asset_metadata_and_text(
    metadata: Dict[str, str],
    extracted_text: str,
    model_name: str = "all-MiniLM-L6-v2",
) -> List[float]:
    """
    Embeds object metadata and extracted text using Sentence Transformers.

    Args:
        metadata: Dictionary of object metadata.
        extracted_text: Text extracted from the object.
        model_name: Sentence Transformer model identifier (default: "all-MiniLM-L6-v2").

    Returns:
        Embedding vector as a list of floats.

    Raises:
        ClientError: If the embedding process fails.
    """
    try:
        model = SentenceTransformer(model_name)

        # Combine metadata and text into a single string
        metadata_str = " ".join(f"{k}: {v}" for k, v in metadata.items())
        combined_text = f"{metadata_str} {extracted_text}".strip()

        embedding = model.encode(combined_text, convert_to_numpy=True)
        return embedding.tolist()
    except Exception as e:
        raise ClientError(
            error_response={"Error": {"Code": "EMBEDDING_FAILED", "Message": str(e)}},
            operation_name="embed_asset_metadata_and_text",
        )
