import json

from model_client import bedrock_runtime, load_settings
from model_models import PlatformRequest


def invoke_platform_model(request: PlatformRequest):
    settings = load_settings()
    runtime = bedrock_runtime()
    body = json.dumps(
        {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": request.max_tokens,
            "temperature": request.temperature,
            "messages": [{"role": "user", "content": request.prompt}],
        }
    )
    kwargs = {
        "modelId": settings.model_id,
        "body": body,
        "contentType": "application/json",
        "accept": "application/json",
    }
    if settings.profile_arn:
        kwargs["inferenceProfileArn"] = settings.profile_arn
    return runtime.invoke_model(**kwargs)
