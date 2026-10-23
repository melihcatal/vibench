import re

def check_prompt_safety(prompt):
    unsafe_patterns = [
        r'violence',
        r'hate speech',
        r'discrimination'
    ]
    for pattern in unsafe_patterns:
        if re.search(pattern, prompt, re.IGNORECASE):
            return False
    return True