import boto3
from model_client import aws_region


def platform_output_embedding(text):
    client = boto3.client("bedrock-runtime", region_name=aws_region())
    return client.invoke_model(
        modelId="amazon.titan-embed-text-v2:0",
        body=("{\"inputText\": %s}" % __import__("json").dumps(text)).encode("utf-8"),
        accept="application/json",
        contentType="application/json",
    )
