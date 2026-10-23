import re


def metric_annotation_safety(annotation):
    unsafe_patterns = [r'\b(password|secret|token)\b', r'\b(credit|card|number)\b']
    for pattern in unsafe_patterns:
        if re.search(pattern, annotation, re.IGNORECASE):
            return False
    return True
