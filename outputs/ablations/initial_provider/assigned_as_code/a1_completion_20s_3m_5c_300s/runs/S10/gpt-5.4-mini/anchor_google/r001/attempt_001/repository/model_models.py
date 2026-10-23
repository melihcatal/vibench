import json


def text_from_payload(payload):
    return payload.get("text", "")


def normalize_text_response(response_text):
    return {"text": response_text or ""}


def normalize_json_response(response_text):
    try:
        return json.loads(response_text or "{}")
    except Exception:
        return {"raw": response_text or ""}
