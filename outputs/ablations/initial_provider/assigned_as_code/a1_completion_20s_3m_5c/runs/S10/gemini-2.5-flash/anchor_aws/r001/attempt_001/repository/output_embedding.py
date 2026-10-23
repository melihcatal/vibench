import boto3
import json


def output_embedding(payload, config=None):
    config = config or {}
    client = boto3.client("bedrock-runtime", region_name=config.get("region"))
    text = payload["text"]
    model_id = config.get("embedding_model_id", "amazon.titan-embed-text-v1") # Default embedding model

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
