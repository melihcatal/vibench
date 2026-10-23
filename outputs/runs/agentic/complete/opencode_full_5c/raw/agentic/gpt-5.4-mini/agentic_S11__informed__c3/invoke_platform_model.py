import json

from model_client import bedrock_client, load_config
from model_models import PlatformRequest, PlatformResponse
from select_platform_resource import select_platform_resource


def invoke_platform_model(request: PlatformRequest) -> PlatformResponse:
    config = load_config()
    resource = select_platform_resource(request.model_id)
    client = bedrock_client(config["region"])
    body = json.dumps(
        {
            "messages": [
                {"role": "user", "content": [{"type": "text", "text": request.prompt}]}
            ],
            "max_tokens": 512,
        }
    )
    response = client.invoke_model(
        modelId=resource["resource_id"],
        body=body,
        accept="application/json",
        contentType="application/json",
    )
    payload = json.loads(response["body"].read())
    text = (
        payload.get("output", {})
        .get("message", {})
        .get("content", [{}])[0]
        .get("text", "")
    )
    return PlatformResponse(
        text=text,
        model_id=resource["model_id"],
        resource_id=resource["resource_id"],
        usage=payload.get("usage"),
        raw=payload,
    )
