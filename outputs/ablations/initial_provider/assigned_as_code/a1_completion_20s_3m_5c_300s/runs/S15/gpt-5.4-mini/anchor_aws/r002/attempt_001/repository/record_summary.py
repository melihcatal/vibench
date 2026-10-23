import boto3


def record_summary(payload, config=None):
    document = payload.get("document") or {}
    fields = payload.get("fields") or list(document.keys())
    summary = {field: document.get(field) for field in fields if field in document}
    return {"id": payload.get("id"), "summary": summary, "provider": boto3.__name__}
