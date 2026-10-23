import re


def payload_safety(decrypted_text):
    unsafe_patterns = [r"malware", r"phishing", r"ransomware"]
    for pattern in unsafe_patterns:
        if re.search(pattern, decrypted_text, re.IGNORECASE):
            return False
    return True
