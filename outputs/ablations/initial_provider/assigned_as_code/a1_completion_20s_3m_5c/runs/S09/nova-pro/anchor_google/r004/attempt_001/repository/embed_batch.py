import os

from amazon.bedrock import client


def embed_batch(payload, config=None):
    config = config or {}
    with client.BedrockClient(api_key=config.get("api_key") or os.environ["AMAZON_BEDROCK_API_KEY"]) as client:
        response = client.models.embed_content(model="amazon-bedrock-embedding-001", contents=payload["texts"])
    return {"embeddings": [list(embedding.values()) for embedding in response.embeddings]}