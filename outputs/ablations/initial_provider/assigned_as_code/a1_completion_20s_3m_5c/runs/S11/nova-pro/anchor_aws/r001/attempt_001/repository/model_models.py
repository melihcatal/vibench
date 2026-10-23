def normalize_payload(payload):
    return {
        "text": payload.get("text", ""),
    }

def normalize_response(response):
    return {
        "text": "".join(block["text"] for block in response["output"]["message"]["content"] if "text" in block),
    }