import re


def metric_annotation_safety(text: str):
    unsafe = bool(re.search(r"(?i)(<script|javascript:|\btoken\b|\bpassword\b)", text))
    return {"safe": not unsafe, "reason": None if not unsafe else "potentially unsafe annotation text"}
