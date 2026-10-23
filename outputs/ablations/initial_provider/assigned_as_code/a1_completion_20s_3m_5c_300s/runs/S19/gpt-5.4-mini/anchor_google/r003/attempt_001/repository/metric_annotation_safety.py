import re


def metric_annotation_safety(payload, config=None):
    text = str(payload.get("text", ""))
    unsafe = bool(re.search(r"(<script|javascript:|data:|on\w+=|\bDROP\b|\bDELETE\b)", text, re.IGNORECASE))
    return {"safe": not unsafe, "reason": "unsafe content detected" if unsafe else "ok"}
