import re

AWS_SAFETY_RE = re.compile(r"^(?!.*(?:\b(?:password|secret|token|api[_-]?key)\b)).{1,280}$", re.IGNORECASE)


def metric_annotation_safety(text: str) -> bool:
    return bool(AWS_SAFETY_RE.match(text or ""))
