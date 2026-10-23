from safety_client import get_openai_client
from typing import List[float]

def moderation_reason_embedding(reason: str) -> List[float]:
    client = get_openai_client()
    if client is None:
        raise ValueError("OpenAI API key not configured")
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=reason
    )
    return [float(x) for x in response.data[0].embedding]
