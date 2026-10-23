import os

import boto3


def translation_memory_embedding(text, region_name=None):
    bedrock = boto3.client("bedrock-runtime", region_name=region_name or os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1")
    return bedrock.invoke_model(body=b'{"inputText":"' + str(text).encode("utf-8") + b'"}', modelId="amazon.titan-embed-text-v1", accept="application/json", contentType="application/json")
