import re


def metric_annotation_safety(annotation):
    unsafe_patterns = [r'\b(badword1|badword2)\b', r'\b(badword3|badword4)\b']
    for pattern in unsafe_patterns:
        if re.search(pattern, annotation, re.IGNORECASE):
            return False
    return True