import json

from model_client import bedrock_runtime, load_settings


def collect_platform_metadata(prompt: str):
    settings = load_settings()
    runtime = bedrock_runtime()
    response = runtime.invoke_model(
        modelId=settings.model_id,
        body=json.dumps(
            {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 128,
                "messages": [{"role": "user", "content": prompt}],
            }
        ),
        contentType="application/json",
        accept="application/json",
    )
    payload = json.loads(response["body"].read())
    return {
        "model_id": settings.model_id,
        "usage": payload.get("usage"),
        "response": payload,
        "request_id": response.get("ResponseMetadata", {}).get("RequestId"),
    }
