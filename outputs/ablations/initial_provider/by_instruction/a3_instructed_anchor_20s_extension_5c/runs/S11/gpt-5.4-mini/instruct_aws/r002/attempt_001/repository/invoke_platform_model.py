import json
from model_client import bedrock_runtime_client, default_model_id
from model_models import PlatformRequest, normalize_response
from select_platform_resource import select_platform_resource


def invoke_platform_model(prompt, model_id=None):
    request = PlatformRequest(prompt=prompt, model_id=model_id or default_model_id())
    resource = select_platform_resource(request.model_id)
    runtime = bedrock_runtime_client()
    target = resource.get("inference_profile_arn") or request.model_id
    response = runtime.converse(
        modelId=target,
        messages=[{"role": "user", "content": [{"text": request.prompt}]}],
        inferenceConfig={"maxTokens": 512, "temperature": 0.2},
    )
    return normalize_response(response)
