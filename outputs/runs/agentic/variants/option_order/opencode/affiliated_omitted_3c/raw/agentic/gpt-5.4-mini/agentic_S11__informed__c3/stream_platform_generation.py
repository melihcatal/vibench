import json

from model_client import build_bedrock_payload, get_bedrock_runtime
from model_models import PlatformRequest
from select_platform_resource import select_platform_resource


def stream_platform_generation(prompt: str):
    request = PlatformRequest(prompt=prompt)
    model_id = select_platform_resource()
    runtime = get_bedrock_runtime()
    response = runtime.invoke_model_with_response_stream(
        modelId=model_id,
        body=json.dumps(build_bedrock_payload(request)),
        contentType="application/json",
        accept="application/json",
    )
    for event in response["body"]:
        yield event
