import json
import sys

from embeddings_client import invoke_embeddings
from embeddings_models import cosine_similarity, normalize_embedding


def embed(text: str):
    result = invoke_embeddings({"inputText": text}, model_id="amazon.titan-embed-text-v2:0")
    embedding = result.get("embedding", result.get("embeddings", [result]))
    if embedding and isinstance(embedding[0], list):
        embedding = embedding[0]
    return normalize_embedding(embedding)


def main() -> None:
    left = sys.argv[1] if len(sys.argv) > 1 else ""
    right = sys.argv[2] if len(sys.argv) > 2 else ""
    score = cosine_similarity(embed(left), embed(right))
    sys.stdout.write(json.dumps({"similarity": score}))


if __name__ == "__main__":
    main()
