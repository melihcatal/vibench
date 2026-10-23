import boto3
import json

def embed_output(payload, config=None):
    config = config or {}
    client = boto3.client("bedrock-runtime", region_name=config.get("region"))
    body = json.dumps({"inputText": payload["text"]})
    response = client.invoke_model(
        body=body,
        modelId="amazon.titan-embed-text-v1",
        accept="application/json",
        contentType="application/json",
    )
    response_body = json.loads(response.get("body").read())
    embedding = response_body.get("embedding")
    return {"embedding": embedding}
