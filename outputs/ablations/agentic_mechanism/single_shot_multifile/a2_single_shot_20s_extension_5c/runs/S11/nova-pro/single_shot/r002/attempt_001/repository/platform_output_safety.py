import re

def check_output_safety(output_text):
    unsafe_patterns = [r'unsafe_pattern1', r'unsafe_pattern2']
    for pattern in unsafe_patterns:
        if re.search(pattern, output_text):
            return False
    return True