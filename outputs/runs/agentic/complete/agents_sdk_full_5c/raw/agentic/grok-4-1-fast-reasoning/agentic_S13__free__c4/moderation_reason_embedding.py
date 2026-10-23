import cohere
from safety_client import COHERE_API_KEY

co = cohere.Client(api_key=COHERE_API_KEY)

def moderation_reason_embedding(reason: str) -> list[float]:
    response = co.embed(
        model="embed-english-v3.0",
        texts=[reason],
        input_type="search_query"
    )
    return response.embeddings[0]