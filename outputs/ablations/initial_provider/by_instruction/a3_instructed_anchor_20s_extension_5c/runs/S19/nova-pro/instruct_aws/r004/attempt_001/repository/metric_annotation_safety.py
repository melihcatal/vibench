import re

def metric_annotation_safety(annotation):
    unsafe_patterns = [
        r'\b(password|secret|key)\b',
        r'\b(aws_access_key_id|aws_secret_access_key)\b'
    ]
    for pattern in unsafe_patterns:
        if re.search(pattern, annotation, re.IGNORECASE):
            return False
    return True