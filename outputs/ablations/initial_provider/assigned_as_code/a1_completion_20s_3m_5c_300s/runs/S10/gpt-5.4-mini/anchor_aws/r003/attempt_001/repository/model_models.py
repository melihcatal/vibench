def normalize_text_response(response):
    if isinstance(response, dict) and "output" in response:
        content = response.get("output", {}).get("message", {}).get("content", [])
        return {"text": "".join(block.get("text", "") for block in content if isinstance(block, dict))}
    return {"text": str(response)}


def normalize_json_response(text):
    return {"json": text}
