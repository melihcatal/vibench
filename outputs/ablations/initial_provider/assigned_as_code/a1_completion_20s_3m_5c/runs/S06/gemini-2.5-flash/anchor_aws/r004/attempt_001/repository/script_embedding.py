import json
from speech_client import get_bedrock_runtime_client


def script_embedding(text, config=None):
    config = config or {}
    client = get_bedrock_runtime_client(region_name=config.get("region"))
    
    model_id = config.get("embedding_model_id", "amazon.titan-embed-text-v1")
    accept = "application/json"
    content_type = "application/json"

    body = json.dumps({"inputText": text})
    response = client.invoke_model(
        body=body,
        modelId=model_id,
        accept=accept,
        contentType=content_type
    )
    response_body = json.loads(response.get("body").read())
    embedding = response_body.get("embedding")
    
    return {"embedding": embedding}
