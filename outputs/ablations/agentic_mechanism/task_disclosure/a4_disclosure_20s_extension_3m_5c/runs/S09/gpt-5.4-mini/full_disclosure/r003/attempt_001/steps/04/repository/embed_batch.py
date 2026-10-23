import json
import os
import sys
from typing import Any, Dict, List, Optional, Sequence

from openai import OpenAI


def embed_batch(texts: Sequence[str], model: Optional[str] = None) -> Dict[str, Any]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    embedding_model = model or os.environ.get("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
    response = client.embeddings.create(model=embedding_model, input=list(texts))
    embeddings: List[Dict[str, Any]] = []
    for item in response.data:
        embeddings.append({"index": item.index, "embedding": item.embedding})
    return {"model": embedding_model, "texts": list(texts), "embeddings": embeddings}


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit("usage: python embed_batch.py <text1> [<text2> ...]")
    result = embed_batch(sys.argv[1:])
    print(json.dumps(result))


if __name__ == "__main__":
    main()
