import json
from typing import Iterator, Optional

from model_client import bedrock_client, get_model_config


def stream_completion(prompt: str, model_id: Optional[str] = None) -> Iterator[str]:
    config = get_model_config(model_id)
    client = bedrock_client(config.region_name)
    response = client.invoke_model_with_response_stream(
        modelId=config.model_id,
        body=json.dumps(
            {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": config.max_tokens,
                "temperature": config.temperature,
                "top_p": config.top_p,
                "messages": [{"role": "user", "content": [{"type": "text", "text": prompt}]}],
            }
        ),
    )
    for event in response["body"]:
        if "chunk" in event:
            data = json.loads(event["chunk"]["bytes"].decode("utf-8"))
            if data.get("type") == "content_block_delta":
                delta = data.get("delta", {})
                text = delta.get("text")
                if text:
                    yield text
