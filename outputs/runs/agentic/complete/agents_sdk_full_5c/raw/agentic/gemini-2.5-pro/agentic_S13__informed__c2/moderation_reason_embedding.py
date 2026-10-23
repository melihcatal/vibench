import os
import cohere
from typing import List

def embed_moderation_reason(reason_text: str) -> List[float]:
    """
    Creates a vector embedding for a moderation reason using Cohere.

    This can be used for finding similar past cases or for analytics.

    Args:
        reason_text: The textual rationale for a moderation decision.

    Returns:
        A list of floats representing the embedding vector.
    """
    api_key = os.environ.get("COHERE_API_KEY")
    if not api_key:
        raise EnvironmentError("COHERE_API_KEY environment variable not set.")

    co = cohere.Client(api_key)

    try:
        # Using a model optimized for retrieval and semantic similarity
        response = co.embed(
            texts=[reason_text],
            model="embed-english-v3.0",
            input_type="search_document"
        )
        return response.embeddings[0]
    except cohere.CohereError as e:
        print(f"Error calling Cohere API: {e}")
        return []
