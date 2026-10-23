import re

def metric_annotation_safety(annotation):
    unsafe_patterns = [
        re.compile(r".*badword.*"),
        re.compile(r".*vulgar.*"),
    ]
    for pattern in unsafe_patterns:
        if pattern.match(annotation):
            return False
    return True