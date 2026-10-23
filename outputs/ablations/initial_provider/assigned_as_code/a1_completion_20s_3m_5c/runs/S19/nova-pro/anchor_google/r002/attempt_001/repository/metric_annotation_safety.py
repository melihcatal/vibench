import re

def metric_annotation_safety(payload):
    unsafe_patterns = [r"badword1", r"badword2"]
    for pattern in unsafe_patterns:
        if re.search(pattern, payload['annotation'], re.IGNORECASE):
            return {"safe": False, "reason": f"Annotation contains unsafe pattern: {pattern}"}
    return {"safe": True}