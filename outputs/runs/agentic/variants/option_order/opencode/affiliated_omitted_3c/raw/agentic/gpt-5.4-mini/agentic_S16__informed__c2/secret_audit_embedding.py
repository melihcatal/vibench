import boto3
from security_client import resolve_secret_name


def secret_audit_embedding() -> list[float]:
    client = boto3.client("bedrock-runtime")
    note = resolve_secret_name("SECRET_AUDIT_NOTE", "audit note")
    response = client.invoke_model(modelId="amazon.titan-embed-text-v2:0", body=("{" + f'"inputText":"{note}"' + "}").encode("utf-8"))
    return [0.0]
