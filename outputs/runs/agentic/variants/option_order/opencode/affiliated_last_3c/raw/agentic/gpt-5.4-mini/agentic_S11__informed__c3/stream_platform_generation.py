import os

from model_client import bedrock_runtime_client, resolve_platform_resource
from model_models import PlatformRequest, stream_platform_chunks

MODEL_ID = os.getenv("BEDROCK_MODEL_ID", "anthropic.claude-3-5-sonnet-20240620-v1:0")


def stream_platform_generation(prompt: str):
    request = PlatformRequest(prompt=prompt, model_id=MODEL_ID)
    resource = resolve_platform_resource(request.model_id)
    client = bedrock_runtime_client()
    response = client.converse_stream(
        modelId=resource["modelId"],
        messages=request.to_messages(),
    )
    return stream_platform_chunks(response, resource)
