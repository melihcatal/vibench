import json
import os
import sys
from typing import List, Optional

from openai import OpenAI


DEFAULT_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


def embed_batch(texts: List[str], model: str = DEFAULT_EMBEDDING_MODEL) -> List[List[float]]:
    if not isinstance(texts, list):
        raise TypeError("texts must be a list of strings")
    if not texts:
        raise ValueError("texts must not be empty")

    cleaned_texts = []
    for text in texts:
        if not isinstance(text, str):
            raise TypeError("each text must be a string")
        if not text.strip():
            raise ValueError("each text must not be empty")
        cleaned_texts.append(text)

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.embeddings.create(model=model, input=cleaned_texts)
    return [list(item.embedding) for item in response.data]


def main(argv: Optional[List[str]] = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if not args:
        raise SystemExit("usage: embed_batch.py TEXT [TEXT ...]")

    embeddings = embed_batch(args)
    sys.stdout.write(json.dumps({"embeddings": embeddings}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
