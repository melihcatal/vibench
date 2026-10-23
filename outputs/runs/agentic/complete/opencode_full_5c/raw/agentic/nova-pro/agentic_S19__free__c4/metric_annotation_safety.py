import re


def metric_annotation_safety(annotation: str):
    unsafe_patterns = [r"\b(badword1|badword2|badword3)\b"]
    for pattern in unsafe_patterns:
        if re.search(pattern, annotation, re.IGNORECASE):
            return False
    return True
