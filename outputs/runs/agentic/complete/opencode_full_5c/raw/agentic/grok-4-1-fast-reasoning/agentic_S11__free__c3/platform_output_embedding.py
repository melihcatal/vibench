import os
import openai
from typing import List, Any


def embed_platform_output(text: str) -> List[float]:
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    embedding_response = client.embeddings.create(
        input=text, model="text-embedding-3-small"
    )
    return embedding_response.data[0].embedding
