import json
import sys

from embeddings_client import bedrock_model_id, bedrock_runtime_client, embedding_dimensions, normalize_text
from embeddings_models import EmbeddingRequest, EmbeddingResponse


def generate_embedding(text: str) -> EmbeddingResponse:
    client = bedrock_runtime_client()
    payload = {"inputText": normalize_text(text)}
    dimensions = embedding_dimensions()
    if dimensions is not None:
        payload["dimensions"] = dimensions
    response = client.invoke_model(
        modelId=bedrock_model_id(),
        body=json.dumps(payload),
        accept="application/json",
        contentType="application/json",
    )
    body = json.loads(response["body"].read())
    return EmbeddingResponse(model_id=bedrock_model_id(), embedding=[float(v) for v in body["embedding"]])


def main() -> None:
    request = EmbeddingRequest(text=" ".join(sys.argv[1:]))
    result = generate_embedding(request.text)
    print(json.dumps({"model_id": result.model_id, "embedding": result.embedding}))


if __name__ == "__main__":
    main()
