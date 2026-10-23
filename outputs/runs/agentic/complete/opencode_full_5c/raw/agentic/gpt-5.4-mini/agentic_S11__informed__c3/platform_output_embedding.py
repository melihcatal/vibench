import os
import boto3


def embed_platform_output(text: str):
    client = boto3.client(
        "bedrock-runtime",
        region_name=os.getenv(
            "AWS_REGION", os.getenv("AWS_DEFAULT_REGION", "us-east-1")
        ),
    )
    body = '{"inputText": %s}' % __import__("json").dumps(text)
    response = client.invoke_model(
        modelId="amazon.titan-embed-text-v2:0",
        body=body,
        accept="application/json",
        contentType="application/json",
    )
    return __import__("json").loads(response["body"].read())
