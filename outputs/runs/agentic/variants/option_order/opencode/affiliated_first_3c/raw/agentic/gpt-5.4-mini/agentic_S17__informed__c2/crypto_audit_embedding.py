import boto3

from security_models import normalize_text


def crypto_audit_embedding(note: str):
    client = boto3.client("bedrock-runtime", region_name="us-east-1")
    body = normalize_text(note)
    return client.invoke_model(modelId="amazon.titan-embed-text-v1", body=body)
