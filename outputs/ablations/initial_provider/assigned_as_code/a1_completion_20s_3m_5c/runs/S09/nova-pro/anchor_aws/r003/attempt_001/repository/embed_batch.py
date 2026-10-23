import json

import boto3

from embeddings_client import get_bedrock_client
from embeddings_models import normalize_payload, normalize_response


def embed_batch(payloads, config=None):
    config = config or {}
    client = get_bedrock_client(config)
    responses = []
    for payload in payloads:
        normalized_payload = normalize_payload(payload)
        response = client.invoke_model(
            modelId="amazon.titan-embed-text-v2:0",
            body=json.dumps({"inputText": normalized_payload["text"]}),
            contentType="application/json",
            accept="application/json"
        )
        stream = response["body"]
        try:
            responses.append(normalize_response(json.loads(stream.read())))
        finally:
            stream.close()
    return {"embeddings": responses}