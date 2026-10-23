import json

from model_client import build_invoke_payload, load_bedrock_runtime_client, model_id_for_request
from model_models import PlatformRequest, PlatformResponse, normalize_text


def collect_platform_metadata(prompt: str, model_id: str = None, max_tokens: int = 256, temperature: float = 0.2) -> PlatformResponse:
    request = PlatformRequest(prompt=prompt, model_id=model_id, max_tokens=max_tokens, temperature=temperature)
    client = load_bedrock_runtime_client()
    payload = build_invoke_payload(request)
    response = client.invoke_model(
        modelId=model_id_for_request(request),
        body=json.dumps(payload),
        accept="application/json",
        contentType="application/json",
    )
    raw = json.loads(response["body"].read())
    return PlatformResponse(
        text=normalize_text(raw.get("content", raw)),
        raw=raw,
        usage=raw.get("usage"),
        model_id=raw.get("model", model_id_for_request(request)),
        resource_id=response.get("ResponseMetadata", {}).get("RequestId"),
    )
