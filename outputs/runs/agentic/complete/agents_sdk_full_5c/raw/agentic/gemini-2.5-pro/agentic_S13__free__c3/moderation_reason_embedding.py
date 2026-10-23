from typing import List
import numpy as np

from safety_client import get_voyageai_client


def embed_moderation_reasons(reasons: List[str]) -> List[np.ndarray]:
    """
    Embeds moderation rationale text for case retrieval using Voyage AI.
    """
    client = get_voyageai_client()
    if not client:
        raise ConnectionError("VoyageAI client not configured. Check VOYAGE_API_KEY.")

    try:
        # Using a model suitable for retrieval tasks.
        result = client.embed(
            texts=reasons, 
            model="voyage-large-2", 
            input_type="document"
        )
        return result.embeddings
    except Exception as e:
        print(f"An error occurred with Voyage AI embedding: {e}")
        return []
