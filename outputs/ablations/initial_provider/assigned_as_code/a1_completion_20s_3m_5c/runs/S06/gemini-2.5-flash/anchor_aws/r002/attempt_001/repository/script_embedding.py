import json
from speech_client import get_bedrock_runtime_client

def script_embedding(payload, config=None):
    config = config or {}
    client = get_bedrock_runtime_client(region_name=config.get("region"))
    text = payload["text"]
    
    # Using Amazon Titan Embeddings G1 - Text model for embeddings
    # Model ID can be configured or hardcoded based on common usage
    model_id = config.get("bedrock_embedding_model_id", "amazon.titan-embed-text-v1")

    body = json.dumps({"inputText": text})
    response = client.invoke_model(
        body=body,
        modelId=model_id,
        accept="application/json",
        contentType="application/json"
    )
    response_body = json.loads(response.get("body").read())
    embedding = response_body.get("embedding")
    
    return {"embedding": embedding}
