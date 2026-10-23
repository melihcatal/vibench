import cohere
from safety_client import get_api_key
from typing import List


def moderation_reason_embedding(reason: str) -> List[float]:
    co = cohere.Client(get_api_key("cohere"))
    response = co.embed(
        texts=[reason], model="embed-english-v3.0", input_type="search_query"
    )
    return response.embeddings[0]
