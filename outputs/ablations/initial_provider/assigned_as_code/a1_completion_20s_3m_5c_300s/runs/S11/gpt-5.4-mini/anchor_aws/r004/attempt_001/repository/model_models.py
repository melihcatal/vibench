def normalize_messages(payload):
    text = payload.get("text", "")
    return [{"role": "user", "content": [{"text": text}]}]


def build_text_response(text, metadata=None):
    result = {"text": text}
    if metadata:
        result["metadata"] = metadata
    return result


def extract_text_from_response(response):
    output = response.get("output", {}).get("message", {}).get("content", [])
    return "".join(block.get("text", "") for block in output if "text" in block)
