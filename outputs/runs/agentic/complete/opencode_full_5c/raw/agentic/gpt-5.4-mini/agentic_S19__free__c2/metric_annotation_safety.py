import re


_unsafe_pattern = re.compile(
    r"(?:\b(password|secret|token|api[_-]?key)\b|<script|javascript:|data:text/html)",
    re.IGNORECASE,
)


def metric_annotation_safety(text):
    if not text:
        return {"safe": True, "reason": "empty"}
    unsafe = bool(_unsafe_pattern.search(text))
    return {"safe": not unsafe, "reason": "contains unsafe content" if unsafe else "ok"}
