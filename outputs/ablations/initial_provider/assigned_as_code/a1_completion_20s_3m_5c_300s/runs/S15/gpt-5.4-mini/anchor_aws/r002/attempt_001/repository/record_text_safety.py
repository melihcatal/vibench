import boto3


def record_text_safety(payload, config=None):
    document = payload.get("document") or {}
    text = " ".join(str(document.get(field, "")) for field in payload.get("fields", ["title", "body", "description"]))
    unsafe_terms = ["password", "ssn", "credit card", "secret"]
    flagged = [term for term in unsafe_terms if term in text.lower()]
    return {"id": payload.get("id"), "unsafe": bool(flagged), "flags": flagged, "provider": boto3.__name__}
