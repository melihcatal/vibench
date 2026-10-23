import os
from typing import Iterable, List, Optional

from openai import OpenAI


def embed_platform_output(text: str, *, model: Optional[str] = None) -> List[float]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    embedding_model = model or os.environ.get("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
    response = client.embeddings.create(model=embedding_model, input=text)
    return list(response.data[0].embedding)


def embed_platform_outputs(texts: Iterable[str], *, model: Optional[str] = None) -> List[List[float]]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    embedding_model = model or os.environ.get("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
    response = client.embeddings.create(model=embedding_model, input=list(texts))
    return [list(item.embedding) for item in response.data]
