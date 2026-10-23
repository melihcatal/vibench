import os
from typing import List
import cohere

def embed_moderation_reason_embedding(reasons: List[str]) -> List[List[float]]:
    """
    Embeds moderation rationales for searching for similar past cases.

    Args:
        reasons: A list of strings, where each string is a rationale
                 for a moderation decision.

    Returns:
        A list of embeddings, where each embedding is a list of floats.
    """
    api_key = os.environ.get("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set.")

    co = cohere.Client(api_key)

    try:
        # Using a model optimized for retrieval tasks
        response = co.embed(
            texts=reasons,
            model="embed-english-v3.0",
            input_type="search_document"
        )
        return response.embeddings
    except cohere.CohereError as e:
        print(f"An error occurred with the Cohere API: {e}")
        raise
