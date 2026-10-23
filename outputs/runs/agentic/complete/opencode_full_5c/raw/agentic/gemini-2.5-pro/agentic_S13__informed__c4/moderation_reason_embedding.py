import os
from typing import List
import cohere


def moderation_reason_embedding(texts: List[str]) -> List[List[float]]:
    try:
        api_key = os.environ["COHERE_API_KEY"]
    except KeyError:
        raise ValueError("Missing environment variable: COHERE_API_KEY")

    co = cohere.Client(api_key)

    response = co.embed(
        texts=texts, model="embed-english-v3.0", input_type="search_document"
    )

    return response.embeddings
