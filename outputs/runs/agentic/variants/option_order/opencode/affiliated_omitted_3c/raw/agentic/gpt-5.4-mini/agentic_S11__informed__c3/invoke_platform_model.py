import json

from model_client import build_bedrock_payload, get_bedrock_runtime, platform_config
from model_models import PlatformRequest
from select_platform_resource import select_platform_resource


def invoke_platform_model(prompt: str, system_prompt: str = None) -> str:
    request = PlatformRequest(prompt=prompt, system_prompt=system_prompt)
    model_id = select_platform_resource()
    runtime = get_bedrock_runtime()
    body = build_bedrock_payload(request)
    response = runtime.invoke_model(
        modelId=model_id,
        body=json.dumps(body),
        contentType="application/json",
        accept="application/json",
    )
    payload = json.loads(response["body"].read())
    content = payload.get("content") or []
    return "".join(part.get("text", "") for part in content if isinstance(part, dict))
