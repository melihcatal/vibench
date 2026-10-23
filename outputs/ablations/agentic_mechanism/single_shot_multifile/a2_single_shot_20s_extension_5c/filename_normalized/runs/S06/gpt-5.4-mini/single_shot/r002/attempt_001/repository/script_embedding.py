import os
from typing import List

from openai import OpenAI


MODEL = os.environ.get('OPENAI_EMBEDDING_MODEL', 'text-embedding-3-small')


def embed_script(script: str) -> List[float]:
    client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
    resp = client.embeddings.create(model=MODEL, input=script)
    return resp.data[0].embedding
