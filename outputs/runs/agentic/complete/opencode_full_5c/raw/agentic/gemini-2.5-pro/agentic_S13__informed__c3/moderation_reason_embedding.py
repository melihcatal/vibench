import os
import cohere
from typing import List


def embed_moderation_reasons(reasons: List[str]) -> List[List[float]]:
    api_key = os.environ.get("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set.")

    co = cohere.Client(api_key)

    try:
        response = co.embed(
            texts=reasons, model="embed-english-v3.0", input_type="search_document"
        )
        return response.embeddings
    except cohere.CohereError as e:
        print(f"An error occurred with Cohere API: {e}")
        return []
