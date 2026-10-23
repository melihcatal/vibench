import re
from typing import List


def check_unsafe_text(text: str) -> bool:
    """Check for unsafe or malicious patterns in free-text metric labels or annotations."""
    unsafe_patterns = [
        r"<script.*?>.*?</script>",
        r"on\w+=",
        r"javascript:",
        r"\b(?:drop|delete|truncate|insert|update|select)\b.*?\b(?:table|database)\b",
        r"\b(?:exec|execute|system|subprocess)\b",
        r"\b(?:rm|mv|cp|chmod|wget|curl)\b",
        r"\$\{\w+\}",
        r"\b(?:password|secret|token|key)\b.*?=\s*\w+",
    ]
    for pattern in unsafe_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False


def metric_annotation_safety(annotations: List[str]) -> dict:
    """Check free-text metric labels or annotations for unsafe text."""
    results = []
    for annotation in annotations:
        is_unsafe = check_unsafe_text(annotation)
        results.append(
            {
                "annotation": annotation,
                "is_unsafe": is_unsafe,
                "reason": "Unsafe pattern detected" if is_unsafe else "Clean",
            }
        )
    return {
        "results": results,
        "summary": {"unsafe_count": sum(1 for r in results if r["is_unsafe"])},
    }
