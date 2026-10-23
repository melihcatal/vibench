import json

import boto3


def embed_text(payload, config=None):
    config = config or {}
    client = boto3.client("bedrock-runtime", region_name=config.get("region", "us-east-1"))
    response = client.invoke_model(modelId="amazon.titan-embed-text-v2:0",
        body=json.dumps({"inputText": payload["text"]}), contentType="application/json", accept="application/json")
    stream = response["body"]
    try:
        return {"embedding": json.loads(stream.read())["embedding"]}
    finally:
        stream.close()
