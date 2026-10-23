import os

import boto3


def platform_output_embedding(text: str):
    client = boto3.client("bedrock-runtime")
    response = client.invoke_model(
        modelId=os.getenv("BEDROCK_EMBEDDING_MODEL_ID", "amazon.titan-embed-text-v1"),
        body=(
            '{"inputText": "' + text.replace("\\", "\\\\").replace('"', '\\"') + '"}'
        ),
        contentType="application/json",
        accept="application/json",
    )
    return response
