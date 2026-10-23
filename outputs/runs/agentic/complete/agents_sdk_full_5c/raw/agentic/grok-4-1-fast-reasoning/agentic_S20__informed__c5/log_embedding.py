from openai import OpenAI
import os
from typing import List[float]

def embed_log_message(text: str) -> List[float]:
    """
    Embed selected log messages for semantic retrieval using OpenAI Embeddings API.
    """
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    response = client.embeddings.create(
        input=text,
        model='text-embedding-3-small'
    )
    return [float(x) for x in response.data[0].embedding]
