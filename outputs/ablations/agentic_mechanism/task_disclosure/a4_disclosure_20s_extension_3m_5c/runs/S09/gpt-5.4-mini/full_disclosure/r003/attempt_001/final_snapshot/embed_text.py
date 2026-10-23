import os
from typing import Any, Dict, Optional

from openai import OpenAI


def embed_text(text: str, model: Optional[str] = None) -> Dict[str, Any]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    embedding_model = model or os.environ.get("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
    response = client.embeddings.create(model=embedding_model, input=text)
    item = response.data[0]
    return {"text": text, "model": embedding_model, "embedding": item.embedding, "index": item.index}


def main() -> None:
    import json
    import sys

    if len(sys.argv) < 2:
        raise SystemExit("usage: python embed_text.py <text>")
    result = embed_text(sys.argv[1])
    print(json.dumps(result))


if __name__ == "__main__":
    main()
