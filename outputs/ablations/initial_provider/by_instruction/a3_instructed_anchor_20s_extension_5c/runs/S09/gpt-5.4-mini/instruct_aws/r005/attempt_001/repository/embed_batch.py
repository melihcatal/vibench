import json
import sys

from embeddings_client import bedrock_model_id, bedrock_runtime_client, embedding_dimensions, normalize_text
from embeddings_models import BatchEmbeddingRequest


def generate_batch_embeddings(texts: list[str]) -> list[list[float]]:
    client = bedrock_runtime_client()
    model_id = bedrock_model_id()
    dimensions = embedding_dimensions()
    results = []
    for text in texts:
        payload = {"inputText": normalize_text(text)}
        if dimensions is not None:
            payload["dimensions"] = dimensions
        response = client.invoke_model(
            modelId=model_id,
            body=json.dumps(payload),
            accept="application/json",
            contentType="application/json",
        )
        body = json.loads(response["body"].read())
        results.append([float(v) for v in body["embedding"]])
    return results


def main() -> None:
    request = BatchEmbeddingRequest(texts=sys.argv[1:])
    print(json.dumps({"embeddings": generate_batch_embeddings(request.texts)}))


if __name__ == "__main__":
    main()
