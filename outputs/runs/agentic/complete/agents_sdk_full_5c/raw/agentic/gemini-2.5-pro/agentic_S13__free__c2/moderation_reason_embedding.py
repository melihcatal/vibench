import os
import voyageai
from typing import List

def embed_moderation_reasons(reasons: List[str]) -> List[List[float]]:
    """
    Embeds moderation rationales for case retrieval using Voyage AI.

    Args:
        reasons: A list of text strings, where each string is a rationale.

    Returns:
        A list of embeddings, where each embedding is a list of floats.
    """
    api_key = os.getenv("VOYAGE_API_KEY")
    if not api_key:
        raise ValueError("VOYAGE_API_KEY not found in environment.")

    client = voyageai.Client(api_key=api_key)

    # Using a model specialized for retrieval/similarity tasks
    response = client.embed(
        texts=reasons,
        model="voyage-large-2",
        input_type="document"
    )

    return response.embeddings
