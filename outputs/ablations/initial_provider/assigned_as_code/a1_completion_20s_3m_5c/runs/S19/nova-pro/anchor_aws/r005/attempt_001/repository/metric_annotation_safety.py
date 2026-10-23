import re


def metric_annotation_safety(annotation):
    unsafe_patterns = [r"badword1", r"badword2"]
    for pattern in unsafe_patterns:
        if re.search(pattern, annotation, re.IGNORECASE):
            return False
    return True