def normalize_generation_payload(payload):
    payload = payload or {}
    return {"text": payload.get("text") or payload.get("prompt") or "", "model": payload.get("model") or "gemini-2.5-flash"}


def normalize_resource_selection(payload):
    payload = payload or {}
    return {"model": payload.get("model") or payload.get("resource") or "gemini-2.5-flash"}
