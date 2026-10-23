import json

from model_client import bedrock_runtime_client, load_platform_config
from model_models import build_bedrock_messages, normalize_text
from select_platform_resource import select_platform_resource


def invoke_platform_model(prompt: str):
    cfg = load_platform_config()
    resource = select_platform_resource()
    client = bedrock_runtime_client()
    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 512,
        "messages": build_bedrock_messages(normalize_text(prompt)),
    }
    target = resource.get("arn") or resource.get("id") or cfg.model_id
    response = client.invoke_model(
        modelId=target,
        body=json.dumps(body),
        accept="application/json",
        contentType="application/json",
    )
    payload = json.loads(response["body"].read())
    return payload
