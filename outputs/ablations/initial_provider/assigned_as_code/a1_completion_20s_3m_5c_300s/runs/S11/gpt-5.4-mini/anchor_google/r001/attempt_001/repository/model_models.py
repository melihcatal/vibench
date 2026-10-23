def normalize_text_payload(payload):
    if isinstance(payload, dict):
        return payload.get("text", "")
    return str(payload)


def build_generation_request(text, model=None):
    return {"text": normalize_text_payload(text), "model": model}


def parse_platform_response(response):
    return {"text": getattr(response, "text", "") or "", "response": response}
