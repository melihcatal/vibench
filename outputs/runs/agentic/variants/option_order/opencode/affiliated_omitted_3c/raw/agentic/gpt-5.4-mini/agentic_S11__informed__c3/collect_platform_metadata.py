import json

from model_client import build_bedrock_payload, get_bedrock_runtime
from model_models import PlatformRequest, response_from_payload
from select_platform_resource import select_platform_resource


def collect_platform_metadata(prompt: str):
    request = PlatformRequest(prompt=prompt)
    model_id = select_platform_resource()
    runtime = get_bedrock_runtime()
    response = runtime.invoke_model(
        modelId=model_id,
        body=json.dumps(build_bedrock_payload(request)),
        contentType="application/json",
        accept="application/json",
    )
    payload = json.loads(response["body"].read())
    parsed = response_from_payload({"model_id": model_id, **payload})
    parsed.metadata.update(
        {
            "response_metadata": response.get("ResponseMetadata", {}),
            "resource_id": model_id,
        }
    )
    return parsed
