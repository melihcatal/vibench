import os
from typing import List
from openai import OpenAI

def moderation_reason_embedding(reason: str) -> List[float]:
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    response = client.embeddings.create(
        input=reason,
        model='text-embedding-3-small'
    )
    return [float(e) for e in response.data[0].embedding]
