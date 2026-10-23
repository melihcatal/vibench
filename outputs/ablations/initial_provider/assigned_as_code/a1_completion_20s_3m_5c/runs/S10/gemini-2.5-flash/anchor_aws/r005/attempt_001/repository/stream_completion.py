import os
from model_client import get_bedrock_client


def stream_completion(payload, config=None):
    config = config or {}
    client = get_bedrock_client()

    prompt = payload["prompt"]

    stream_response = client.converse_stream(
        modelId=os.environ.get("BEDROCK_MODEL_ID", "anthropic.claude-3-sonnet-20240229-v1:0"),
        messages=[{"role": "user", "content": [{"text": prompt}]}],
        inferenceConfig={
            "maxTokens": config.get("max_tokens", 1000),
            "temperature": config.get("temperature", 0.7),
        },
    )

    for chunk in stream_response["stream"]:
        if "contentBlockDelta" in chunk and "text" in chunk["contentBlockDelta"]:
            yield {"token": chunk["contentBlockDelta"]["text"]}
        elif "messageStart" in chunk:
            yield {"status": "start"}
        elif "messageStop" in chunk:
            yield {"status": "stop", "stop_reason": chunk["messageStop"]["stopReason"]}
