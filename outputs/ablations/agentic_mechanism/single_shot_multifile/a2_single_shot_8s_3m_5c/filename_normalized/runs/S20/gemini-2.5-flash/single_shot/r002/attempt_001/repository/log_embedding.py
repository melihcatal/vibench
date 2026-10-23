from observability_client import get_openai_client
from typing import List

def embed_log_message(text: str) -> List[float]:
    openai_client = get_openai_client()

    response = openai_client.embeddings.create(
        input=[text],
        model="text-embedding-3-small"
    )

    return response.data[0].embedding
