import json

from embeddings_client import bedrock_runtime_client
from embeddings_models import EmbedRequest, EmbedResponse


def embed_text(text: str) -> EmbedResponse:
    client, config = bedrock_runtime_client()
    payload = {"inputText": EmbedRequest(text=text).text}
    response = client.invoke_model(modelId=config.model_id, body=json.dumps(payload))
    body = json.loads(response["body"].read())
    return EmbedResponse(embedding=body["embedding"])
