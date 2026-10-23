import re


def metric_annotation_safety(text: str):
    unsafe = bool(re.search(r"(?i)(<script|javascript:|onerror=|onload=)", text))
    return {"safe": not unsafe, "provider": "google-cloud-monitoring"}
