import cohere
from typing import List
from safety_client import get_api_key


def moderation_reason_embedding(reason: str) -> List[float]:
    api_key = get_api_key("COHERE_API_KEY")
    co = cohere.Client(api_key)
    response = co.embed(
        texts=[reason], model="embed-english-v3.0", input_type="search_query"
    )
    return response.embeddings[0]
