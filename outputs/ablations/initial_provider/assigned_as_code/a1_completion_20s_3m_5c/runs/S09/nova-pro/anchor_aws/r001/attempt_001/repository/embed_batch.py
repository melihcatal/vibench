import json

import boto3

from embeddings_client import get_bedrock_client
from embeddings_models import EmbeddingRequest, EmbeddingResponse


def embed_batch(payloads, config=None):
    config = config or {}
    client = get_bedrock_client(config)
    requests = [EmbeddingRequest(text=payload["text"]).to_dict() for payload in payloads]
    response = client.invoke_model(modelId="amazon.titan-embed-text-v2:0",
                                   body=json.dumps({"inputTexts": [req["text"] for req in requests]},
                                                    default=str),
                                   contentType="application/json",
                                   accept="application/json")
    stream = response["body"]
    try:
        embeddings = json.loads(stream.read())["embeddings"]
        return [{"embedding": embedding} for embedding in embeddings]
    finally:
        stream.close()