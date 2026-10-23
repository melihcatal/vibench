from typing import Any, Dict, Iterator

from model_client import bedrock_runtime_client, load_platform_config


def stream_platform_generation(prompt: str) -> Iterator[Dict[str, Any]]:
    config = load_platform_config()
    client = bedrock_runtime_client()
    response = client.converse_stream(
        modelId=config.model_id,
        messages=[{"role": "user", "content": [{"text": prompt}]}],
    )
    yield response
    for event in response.get("stream", []):
        yield event
