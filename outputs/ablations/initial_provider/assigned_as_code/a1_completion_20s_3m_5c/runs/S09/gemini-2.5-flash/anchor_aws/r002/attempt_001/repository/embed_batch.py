import json

import boto3

from embeddings_client import get_bedrock_client

def embed_batch(payload, config=None):
    config = config or {}
    client = get_bedrock_client(region_name=config.get("region", "us-east-1"))
    
    batch_embeddings = []
    for text in payload["texts"]:
        response = client.invoke_model(modelId="amazon.titan-embed-text-v2:0",
            body=json.dumps({"inputText": text}), contentType="application/json", accept="application/json")
        stream = response["body"]
        try:
            batch_embeddings.append(json.loads(stream.read())["embedding"])
        finally:
            stream.close()
    return {"embeddings": batch_embeddings}
