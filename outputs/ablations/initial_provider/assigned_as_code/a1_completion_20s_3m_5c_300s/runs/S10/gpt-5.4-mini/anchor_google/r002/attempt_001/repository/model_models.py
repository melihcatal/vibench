import json


def normalize_text_response(response):
    return {"text": getattr(response, "text", "") or ""}


def normalize_structured_json_response(response):
    text = getattr(response, "text", "") or ""
    try:
        data = json.loads(text)
    except Exception:
        data = {"raw": text}
    return data


def normalize_stream_chunk(chunk):
    return getattr(chunk, "text", "") or ""


def build_prompt(prefix, text):
    return prefix + text
