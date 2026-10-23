import os
from typing import List

from openai import OpenAI


def embed_text(text: str, model: str = "text-embedding-3-small") -> List[float]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.embeddings.create(model=model, input=text)
    return list(response.data[0].embedding)


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        raise SystemExit("usage: embed_text.py TEXT")
    print(embed_text(sys.argv[1]))
