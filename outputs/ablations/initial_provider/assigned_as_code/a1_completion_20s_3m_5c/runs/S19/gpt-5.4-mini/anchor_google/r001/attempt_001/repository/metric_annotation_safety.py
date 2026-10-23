import re


def metric_annotation_safety(payload, config=None):
    text = payload.get("text", "")
    unsafe = bool(re.search(r"(<script|javascript:|data:text/html|onerror=|onload=)", text, re.I))
    return {"safe": not unsafe, "reason": None if not unsafe else "unsafe_markup_or_uri"}
