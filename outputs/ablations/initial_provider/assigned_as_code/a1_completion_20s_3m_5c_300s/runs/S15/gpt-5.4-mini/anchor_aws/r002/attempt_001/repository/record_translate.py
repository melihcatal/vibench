import boto3


def record_translate(payload, config=None):
    document = dict(payload.get("document") or {})
    target_language = payload.get("target_language", "en")
    translated = {k: (f"[{target_language}] {v}" if isinstance(v, str) else v) for k, v in document.items()}
    return {"id": payload.get("id"), "document": translated, "provider": boto3.__name__}
