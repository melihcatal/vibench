from __future__ import annotations

from typing import List

from openai import OpenAI


EMBEDDING_MODEL = "text-embedding-3-small"


def transcript_embedding(segments: List[str]) -> List[List[float]]:
    client = OpenAI()
    response = client.embeddings.create(model=EMBEDDING_MODEL, input=segments)
    return [item.embedding for item in response.data]


if __name__ == "__main__":
    raise SystemExit("import and call transcript_embedding(segments)")
