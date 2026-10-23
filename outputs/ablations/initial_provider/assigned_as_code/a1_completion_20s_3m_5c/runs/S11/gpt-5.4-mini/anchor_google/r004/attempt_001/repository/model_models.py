def normalize_prompt(payload):
    if isinstance(payload, dict):
        return {"text": str(payload.get("text", ""))}
    return {"text": str(payload)}


def normalize_response(response):
    return {"text": getattr(response, "text", "") or "", "raw": response}
