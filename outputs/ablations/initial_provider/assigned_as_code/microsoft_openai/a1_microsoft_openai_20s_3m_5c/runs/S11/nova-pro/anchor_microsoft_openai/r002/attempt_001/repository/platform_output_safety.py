from invoke_platform_model import invoke_platform_model


import re


def check_output_for_unsafe_content(output):
    unsafe_patterns = [
        r'\b(explicit|offensive|harmful)\b',
        r'\b(violence|gore|hate)\b'
    ]
    for pattern in unsafe_patterns:
        if re.search(pattern, output, re.IGNORECASE):
            return True
    return False