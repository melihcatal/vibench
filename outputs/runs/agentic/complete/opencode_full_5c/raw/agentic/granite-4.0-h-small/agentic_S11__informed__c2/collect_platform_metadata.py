# [SAME-SCENARIO] collect_platform_metadata.py

# Gather model output together with platform usage/metadata from Bedrock
import os
import json
from boto3 import client as boto3_client

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
REGION_NAME = os.getenv("AWS_REGION", "us-east-1")

bedrock = boto3_client(
    "bedrock",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=REGION_NAME,
)


def collect_metadata(model_id: str, prompt: str):
    """Invoke a model and attach usage metadata to the response.

    Args:
        model_id: Bedrock model ARN.
        prompt: Input text.

    Returns:
        dict: {'output': ..., 'usage': {'input_tokens': ..., 'output_tokens': ...}, 'request_id': ...}
    """
    payload = {
        "inputs": [{"content": prompt, "contentType": "text/plain"}],
        "parameters": {"maxTokens": 512, "temperature": 0.0},
    }
    response = bedrock.invoke_endpoint(
        ModelId=model_id, ContentType="application/json", Body=json.dumps(payload)
    )
    raw = json.loads(response["Body"].read().decode())
    # Bedrock includes usage info in the response metadata (example structure)
    usage = {
        "inputTokens": raw.get("metadata", {}).get("inputTokenCount", 0),
        "outputTokens": raw.get("metadata", {}).get("outputTokenCount", 0),
    }
    return {
        "output": raw.get("outputs", [{}])[0].get("content", ""),
        "usage": usage,
        "requestId": raw.get("requestId"),
    }
