import re


def check_payload_safety(payload):
    unsafe_patterns = [r'malware', r'phishing', r'ransomware']
    for pattern in unsafe_patterns:
        if re.search(pattern, payload):
            return False
    return True