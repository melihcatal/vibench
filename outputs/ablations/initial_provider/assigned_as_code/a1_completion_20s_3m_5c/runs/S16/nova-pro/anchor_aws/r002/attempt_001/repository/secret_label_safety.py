import re

def check_secret_labels(payload):
    unsafe_patterns = [r"password", r"secret", r"key"]
    labels = payload.get("labels", [])
    for label in labels:
        if any(re.search(pattern, label, re.IGNORECASE) for pattern in unsafe_patterns):
            return {"status": "unsafe"}
    return {"status": "safe"}