from google.cloud import securitycenter_v1


def metric_annotation_safety(payload, config=None):
    client = securitycenter_v1.SecurityCenterClient()
    text = payload.get("text", "")
    unsafe = any(token in text.lower() for token in ("<script", "javascript:", "data:text/html", "onerror=", "onload="))
    return {"safe": not unsafe, "provider": "google.cloud.securitycenter_v1", "checked": bool(text), "resource_name": getattr(client, "transport", None).__class__.__name__ if client else None}
