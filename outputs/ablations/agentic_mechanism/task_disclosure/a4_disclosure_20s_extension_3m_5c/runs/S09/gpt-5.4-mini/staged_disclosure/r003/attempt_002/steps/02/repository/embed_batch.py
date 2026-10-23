import os
import sys
from typing import List

from openai import OpenAI


def embed_batch(texts: List[str]) -> List[List[float]]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.embeddings.create(model="text-embedding-3-small", input=texts)
    return [item.embedding for item in response.data]


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit("usage: python embed_batch.py <text1> [<text2> ...]")
    print(embed_batch(sys.argv[1:]))
