import json

from embeddings_client import bedrock_runtime_client
from embeddings_models import EmbedBatchRequest, EmbedResponse


def embed_batch(texts: list[str]) -> list[EmbedResponse]:
    client, config = bedrock_runtime_client()
    request = EmbedBatchRequest(texts=texts)
    results: list[EmbedResponse] = []
    for text in request.texts:
        response = client.invoke_model(modelId=config.model_id, body=json.dumps({"inputText": text}))
        body = json.loads(response["body"].read())
        results.append(EmbedResponse(embedding=body["embedding"]))
    return results
