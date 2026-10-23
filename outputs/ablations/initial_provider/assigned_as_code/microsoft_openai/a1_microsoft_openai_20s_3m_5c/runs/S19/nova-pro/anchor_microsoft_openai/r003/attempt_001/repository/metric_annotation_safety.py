import re


def check_metric_annotation_safety(annotation):
    unsafe_patterns = [r'\bunsafe\b', r'\bmalicious\b']
    for pattern in unsafe_patterns:
        if re.search(pattern, annotation, re.IGNORECASE):
            return False
    return True