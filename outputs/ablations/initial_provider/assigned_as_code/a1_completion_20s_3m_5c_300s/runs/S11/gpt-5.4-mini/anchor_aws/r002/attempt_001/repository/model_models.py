def normalize_text_payload(payload):
    if isinstance(payload, str):
        return {"text": payload}
    if isinstance(payload, dict):
        return {"text": payload.get("text", "")}
    return {"text": str(payload)}


def build_converse_messages(text):
    return [{"role": "user", "content": [{"text": text}]}]


def extract_response_text(response):
    if not isinstance(response, dict):
        return ""
    output = response.get("output", {})
    message = output.get("message", {})
    content = message.get("content", [])
    return "".join(block.get("text", "") for block in content if isinstance(block, dict))
