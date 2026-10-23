import os
import json
import boto3
from security_models import SecretRequest, normalize_response


def secret_audit_embedding(request: SecretRequest) -> str:
    """Embed secret audit notes for semantic search.

    Returns a JSON string representing audit metadata.
    """
    secret_name = request["name"]
    client = boto3.client("bedrock-runtime", region_name=os.getenv("AWS_REGION"))
    prompt = f"Summarize audit notes for secret {secret_name} in a concise paragraph."
    response = client.invoke_model(
        Body=json.dumps({"prompt": prompt}),
        ModelId="anthropic.claude-3-5-sonnet-20240620-v1:0",
    )
    result = json.loads(response["Body"].read().decode())
    return result["content"]
