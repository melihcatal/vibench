import re


def check_script_safety(script):
    unsafe_patterns = [
        r"hate speech",
        r"violence",
        r"discrimination"
    ]
    for pattern in unsafe_patterns:
        if re.search(pattern, script, re.IGNORECASE):
            return False
    return True