import json

from model_client import bedrock_client, load_config
from model_models import PlatformRequest
from select_platform_resource import select_platform_resource


def stream_platform_generation(request: PlatformRequest):
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
    response = client.invoke_model_with_response_stream(
        modelId=resource["resource_id"],
        body=body,
        accept="application/json",
        contentType="application/json",
    )
    return response
