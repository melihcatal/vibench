def normalize_text_payload(payload):
    if isinstance(payload, dict):
        if "text" in payload:
            return payload["text"]
        if "input" in payload:
            return payload["input"]
        if "prompt" in payload:
            return payload["prompt"]
    return str(payload)


def extract_bedrock_text(response):
    return "".join(
        block.get("text", "")
        for block in response.get("output", {}).get("message", {}).get("content", [])
        if isinstance(block, dict)
    )


def stream_bedrock_text(event):
    if not isinstance(event, dict):
        return ""
    if "contentBlockDelta" in event:
        delta = event.get("contentBlockDelta", {}).get("delta", {})
        return delta.get("text", "")
    if "chunk" in event:
        chunk = event.get("chunk", {}).get("bytes")
        if isinstance(chunk, bytes):
            return chunk.decode("utf-8")
        if isinstance(chunk, str):
            return chunk
    return ""
