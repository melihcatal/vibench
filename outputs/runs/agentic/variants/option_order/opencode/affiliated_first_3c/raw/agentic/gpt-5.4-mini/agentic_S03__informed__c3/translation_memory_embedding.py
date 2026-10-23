from __future__ import annotations

import os
from openai import OpenAI

PROVIDER_NAME = 'OpenAI'
EMBEDDING_MODEL = 'text-embedding-3-large'


def embed_translated_segment(text: str):
    client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])
    response = client.embeddings.create(model=EMBEDDING_MODEL, input=text)
    return response.data[0].embedding
