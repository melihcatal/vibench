import os
from typing import List, Sequence

from openai import OpenAI


OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


def embed_script(script: str) -> List[float]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.embeddings.create(model=OPENAI_EMBEDDING_MODEL, input=script)
    return list(response.data[0].embedding)


def embed_scripts(scripts: Sequence[str]) -> List[List[float]]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.embeddings.create(model=OPENAI_EMBEDDING_MODEL, input=list(scripts))
    return [list(item.embedding) for item in response.data]
