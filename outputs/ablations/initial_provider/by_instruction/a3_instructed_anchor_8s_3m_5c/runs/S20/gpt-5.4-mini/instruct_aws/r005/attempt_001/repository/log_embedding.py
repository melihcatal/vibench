from __future__ import annotations

import boto3


def log_embedding(texts: list[str]):
    client = boto3.client("bedrock-runtime", region_name="us-east-1")
    embeddings = []
    for text in texts:
        response = client.invoke_model(
            modelId="amazon.titan-embed-text-v1",
            contentType="application/json",
            accept="application/json",
            body=(f'{{"inputText": {text!r}}}').replace("'", '"'),
        )
        embeddings.append(response["body"].read())
    return embeddings
