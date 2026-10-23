import json
import sys

from embeddings_client import batch_texts, invoke_embeddings
from embeddings_models import BatchEmbeddingRequest, normalize_embedding


def main() -> None:
    texts = sys.argv[1:] or [""]
    request = BatchEmbeddingRequest(texts=batch_texts(texts))
    outputs = []
    for text in request.texts:
        result = invoke_embeddings({"inputText": text}, model_id="amazon.titan-embed-text-v2:0")
        embedding = result.get("embedding", result.get("embeddings", [result]))
        if embedding and isinstance(embedding[0], list):
            embedding = embedding[0]
        outputs.append(normalize_embedding(embedding))
    sys.stdout.write(json.dumps({"embeddings": outputs}))


if __name__ == "__main__":
    main()
