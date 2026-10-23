import boto3

from security_client import aws_region


def crypto_audit_embedding(notes: str):
    bedrock = boto3.client("bedrock-runtime", region_name=aws_region())
    body = {"inputText": notes}
    return bedrock.invoke_model(body=str(body).encode(), modelId="amazon.titan-embed-text-v2:0", accept="application/json", contentType="application/json")
