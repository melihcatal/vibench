import json
import sys

from embeddings_client import invoke_embeddings
from embeddings_models import normalize_embedding


def embed(text: str):
    result = invoke_embeddings({"inputText": text}, model_id="amazon.titan-embed-text-v2:0")
    embedding = result.get("embedding", result.get("embeddings", [result]))
    if embedding and isinstance(embedding[0], list):
        embedding = embedding[0]
    return normalize_embedding(embedding)


def main() -> None:
    query = sys.argv[1] if len(sys.argv) > 1 else ""
    documents = sys.argv[2:]
    sys.stdout.write(json.dumps({"query_embedding": embed(query), "document_embeddings": [embed(doc) for doc in documents]}))


if __name__ == "__main__":
    main()
