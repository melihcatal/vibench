import json
import sys

from embeddings_client import invoke_embeddings
from embeddings_models import EmbeddingRequest, EmbeddingResponse, normalize_embedding


def main() -> None:
    text = sys.argv[1] if len(sys.argv) > 1 else ""
    request = EmbeddingRequest(text=text)
    payload = {"inputText": request.text}
    result = invoke_embeddings(payload, model_id="amazon.titan-embed-text-v2:0")
    embedding = result.get("embedding", result.get("embeddings", [result]))
    if embedding and isinstance(embedding[0], list):
        embedding = embedding[0]
    response = EmbeddingResponse(embedding=normalize_embedding(embedding))
    sys.stdout.write(json.dumps({"embedding": response.embedding}))


if __name__ == "__main__":
    main()
