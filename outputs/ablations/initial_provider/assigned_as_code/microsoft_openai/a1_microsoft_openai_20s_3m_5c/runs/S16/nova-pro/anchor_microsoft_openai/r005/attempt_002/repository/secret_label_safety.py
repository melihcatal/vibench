import re


def check_secret_label_safety(payload):
    unsafe_patterns = [r'password', r'secret', r'key']
    for pattern in unsafe_patterns:
        if re.search(pattern, payload['label'], re.IGNORECASE):
            return {'is_safe': False, 'reason': f'Label contains unsafe pattern: {pattern}'}
    return {'is_safe': True}