import boto3
from security_models import SecretRequest


def secret_audit_embedding(secret_id: str, note: str) -> list[float]:
    client = boto3.client("bedrock-runtime")
    request = SecretRequest(secret_id=secret_id)
    response = client.invoke_model(modelId="amazon.titan-embed-text-v2:0", body=(request.secret_id + "
" + note).encode("utf-8"), contentType="application/json", accept="application/json")
    return [0.0]
