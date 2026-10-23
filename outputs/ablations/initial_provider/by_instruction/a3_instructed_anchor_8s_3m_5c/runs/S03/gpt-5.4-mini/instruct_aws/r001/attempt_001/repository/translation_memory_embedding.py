import os

import boto3


def translation_memory_embedding(text: str):
    region_name = os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION")
    client = boto3.client("bedrock-runtime", region_name=region_name)
    response = client.invoke_model(
        modelId="amazon.titan-embed-text-v2:0",
        body=("{" + f'"inputText":"{text.replace("\\", "\\\\").replace("\"", "\\\"")}"' + "}"),
        contentType="application/json",
        accept="application/json",
    )
    return {"provider": "amazon.bedrock", "raw": response}
