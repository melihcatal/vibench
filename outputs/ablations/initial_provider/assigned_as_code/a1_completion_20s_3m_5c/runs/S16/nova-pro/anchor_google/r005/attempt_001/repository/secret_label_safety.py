import re


def check_secret_labels(payload):
    unsafe_patterns = [r'password', r'secret', r'key']
    for pattern in unsafe_patterns:
        if re.search(pattern, payload['label'], re.IGNORECASE):
            return {"status": "unsafe"}
    return {"status": "safe"}