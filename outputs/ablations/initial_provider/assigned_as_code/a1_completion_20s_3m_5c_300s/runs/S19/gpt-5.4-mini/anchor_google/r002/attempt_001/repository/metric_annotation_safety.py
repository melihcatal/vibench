import re

from google.cloud import monitoring_v3


_UNSAFE = re.compile(r"(?:<script|javascript:|\bDROP\b|\bUNION\b|\bSELECT\b)", re.IGNORECASE)


def metric_annotation_safety(payload, config=None):
    text = payload.get("text", "")
    return {"safe": _UNSAFE.search(text) is None, "provider": "google-cloud-monitoring"}
