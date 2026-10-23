import re


def secret_label_safety(payload):
    unsafe_patterns = [r'password', r'secret', r'key']
    for pattern in unsafe_patterns:
        if re.search(pattern, payload['label'], re.IGNORECASE):
            return {'safe': False}
    return {'safe': True}