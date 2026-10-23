import json

from model_client import bedrock_runtime, load_settings


def stream_platform_generation(prompt: str):
    settings = load_settings()
    runtime = bedrock_runtime()
    body = json.dumps(
        {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 256,
            "messages": [{"role": "user", "content": prompt}],
        }
    )
    response = runtime.invoke_model_with_response_stream(
        modelId=settings.model_id,
        body=body,
        contentType="application/json",
        accept="application/json",
    )
    return response
