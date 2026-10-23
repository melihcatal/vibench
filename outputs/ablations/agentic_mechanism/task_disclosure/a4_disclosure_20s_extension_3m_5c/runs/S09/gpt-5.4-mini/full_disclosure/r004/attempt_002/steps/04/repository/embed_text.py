import os
from typing import Any, Dict, List, Optional

from openai import OpenAI


DEFAULT_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


def embed_text(text: str, model: str = DEFAULT_EMBEDDING_MODEL) -> List[float]:
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    if not text.strip():
        raise ValueError("text must not be empty")

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.embeddings.create(model=model, input=text)
    return list(response.data[0].embedding)


def main(argv: Optional[List[str]] = None) -> int:
    import json
    import sys

    args = sys.argv[1:] if argv is None else argv
    if not args:
        raise SystemExit("usage: embed_text.py TEXT")

    embedding = embed_text(args[0])
    sys.stdout.write(json.dumps({"embedding": embedding}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
