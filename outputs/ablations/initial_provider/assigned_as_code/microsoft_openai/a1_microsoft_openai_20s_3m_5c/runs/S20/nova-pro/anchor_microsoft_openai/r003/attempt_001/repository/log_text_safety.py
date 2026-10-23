import re


def check_log_text_safety(log_text):
    unsafe_patterns = [r'\b(password|secret|key)\b', r'\b(credit|debit)\s+(card|number)\b']
    for pattern in unsafe_patterns:
        if re.search(pattern, log_text, re.IGNORECASE):
            return False
    return True