import json

from model_client import stream_bedrock, model_id
from model_models import anthropic_messages_prompt, clean_text


def stream_completion(prompt, max_tokens=256, temperature=0.2):
    payload = anthropic_messages_prompt(
        "Continue the user's request.",
        clean_text(prompt),
        max_tokens=max_tokens,
        temperature=temperature,
    )
    for event in stream_bedrock(model_id("stream"), payload):
        chunk = event.get("chunk") if isinstance(event, dict) else None
        if chunk and "bytes" in chunk:
            data = json.loads(chunk["bytes"].decode("utf-8"))
            delta = data.get("delta", {})
            text = delta.get("text")
            if text:
                yield text
