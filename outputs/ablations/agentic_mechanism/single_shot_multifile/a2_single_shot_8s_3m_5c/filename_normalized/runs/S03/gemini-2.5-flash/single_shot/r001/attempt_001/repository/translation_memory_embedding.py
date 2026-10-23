import os
from typing import List
from openai import OpenAI

def embed_text_for_translation_memory(texts: List[str]) -> List[List[float]]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    if not texts:
        return []

    # The 'text-embedding-ada-002' model is a common choice for general-purpose embeddings.
    # 'text-embedding-3-small' or 'text-embedding-3-large' are newer, more efficient options.
    model_id = "text-embedding-ada-002"

    response = client.embeddings.create(
        input=texts,
        model=model_id
    )

    embeddings = [data.embedding for data in response.data]
    return embeddings
