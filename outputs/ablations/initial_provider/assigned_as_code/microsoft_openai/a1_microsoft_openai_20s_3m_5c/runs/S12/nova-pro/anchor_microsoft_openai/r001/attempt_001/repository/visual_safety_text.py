import re


def visual_safety_text(payload, config=None):
    unsafe_patterns = [re.compile(pattern) for pattern in config['unsafe_patterns']]
    for pattern in unsafe_patterns:
        if pattern.search(payload['text']):
            return {'unsafe': True}
    return {'unsafe': False}