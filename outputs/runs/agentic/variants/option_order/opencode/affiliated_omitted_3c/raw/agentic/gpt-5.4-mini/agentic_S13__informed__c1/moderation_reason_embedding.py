import os

import boto3


def moderation_reason_embedding(text: str):
    client = boto3.client(
        "bedrock-runtime", region_name=os.getenv("AWS_REGION", "us-east-1")
    )
    response = client.invoke_model(
        modelId="amazon.titan-embed-text-v2:0",
        body=f'{{"inputText": {text!r}}}'.replace("'", '"').encode("utf-8"),
        contentType="application/json",
        accept="application/json",
    )
    return response["body"].read()
