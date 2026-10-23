import json
import os

import boto3


def output_embedding(text: str):
    client = boto3.client("bedrock-runtime", region_name=os.environ.get("AWS_REGION", "us-east-1"))
    response = client.invoke_model(
        modelId=os.environ.get("AWS_BEDROCK_EMBEDDING_MODEL_ID", "amazon.titan-embed-text-v2:0"),
        body=json.dumps({"inputText": text}),
    )
    body = json.loads(response["body"].read())
    return body.get("embedding", [])
