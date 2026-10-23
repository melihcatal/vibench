import json
import os
import sys
from typing import List

from openai import OpenAI


def embed_text(text: str) -> List[float]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.embeddings.create(model="text-embedding-3-small", input=text)
    return response.data[0].embedding


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit("usage: python embed_text.py <text>")
    embedding = embed_text(sys.argv[1])
    print(json.dumps(embedding))


if __name__ == "__main__":
    main()
