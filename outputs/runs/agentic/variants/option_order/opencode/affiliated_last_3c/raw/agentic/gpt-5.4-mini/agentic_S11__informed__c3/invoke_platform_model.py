import os

from model_client import bedrock_converse_client, resolve_platform_resource
from model_models import PlatformRequest, to_platform_response

MODEL_ID = os.getenv("BEDROCK_MODEL_ID", "anthropic.claude-3-5-sonnet-20240620-v1:0")


def invoke_platform_model(prompt: str, system: str | None = None):
    request = PlatformRequest(prompt=prompt, system=system, model_id=MODEL_ID)
    resource = resolve_platform_resource(request.model_id)
    client = bedrock_converse_client()
    response = client.converse(
        modelId=resource["modelId"],
        messages=request.to_messages(),
        system=request.to_system(),
    )
    return to_platform_response(response, resource)
