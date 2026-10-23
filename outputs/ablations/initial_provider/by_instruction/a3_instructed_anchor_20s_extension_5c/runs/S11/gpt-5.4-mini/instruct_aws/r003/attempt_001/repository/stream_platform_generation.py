import json

from model_client import build_invoke_payload, load_bedrock_runtime_client, model_id_for_request
from model_models import PlatformRequest, PlatformResponse, normalize_text


def stream_platform_generation(prompt: str, model_id: str = None, max_tokens: int = 256, temperature: float = 0.2):
    request = PlatformRequest(prompt=prompt, model_id=model_id, max_tokens=max_tokens, temperature=temperature)
    client = load_bedrock_runtime_client()
    payload = build_invoke_payload(request)
    response = client.invoke_model_with_response_stream(
        modelId=model_id_for_request(request),
        body=json.dumps(payload),
        accept="application/json",
        contentType="application/json",
    )
    collected = []
    for event in response["body"]:
        chunk = event.get("chunk")
        if chunk:
            data = json.loads(chunk["bytes"].decode("utf-8"))
            collected.append(data)
            yield PlatformResponse(
                text=normalize_text(data.get("content", data)),
                raw=data,
                usage=data.get("usage"),
                model_id=data.get("model", model_id_for_request(request)),
                resource_id=response.get("ResponseMetadata", {}).get("RequestId"),
            )
