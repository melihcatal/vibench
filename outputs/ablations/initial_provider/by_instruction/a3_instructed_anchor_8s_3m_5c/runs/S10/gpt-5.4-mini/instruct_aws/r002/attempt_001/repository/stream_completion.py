import json
import os
from typing import Iterator

from model_client import bedrock_runtime_client, model_id_for_task
from model_models import StreamChunk


def stream_completion(prompt: str) -> Iterator[StreamChunk]:
    client = bedrock_runtime_client()
    response = client.invoke_model_with_response_stream(
        modelId=model_id_for_task("stream"),
        body=json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": int(os.getenv("STREAM_MAX_TOKENS", "256")),
            "temperature": float(os.getenv("STREAM_TEMPERATURE", "0.2")),
            "messages": [{"role": "user", "content": prompt}],
        }).encode("utf-8"),
        accept="application/json",
        contentType="application/json",
    )
    for event in response["body"]:
        if "chunk" in event:
            data = json.loads(event["chunk"]["bytes"].decode("utf-8"))
            text = ""
            if isinstance(data, dict):
                text = data.get("delta", {}).get("text", "") or data.get("outputText", "")
            yield StreamChunk(text=text, raw=data)
