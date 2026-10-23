import json

from model_client import bedrock_runtime_client, get_config
from model_models import TextRequest, TextResponse


DEFAULT_MODEL_ID = "amazon.titan-embed-text-v1"


def output_embedding(request: TextRequest) -> TextResponse:
    config = get_config(DEFAULT_MODEL_ID)
    client = bedrock_runtime_client(config.region)
    response = client.invoke_model(modelId=config.model_id, body=json.dumps({"inputText": request.text}))
    body = json.loads(response["body"].read())
    embedding = body.get("embedding") or body.get("embeddings")
    return TextResponse(text=json.dumps(embedding), raw=body)
