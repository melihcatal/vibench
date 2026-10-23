import re


def payload_safety(text: str) -> bool:
    unsafe = [r"\bpassword\b", r"\bsecret\b", r"\bssn\b", r"\bprivate key\b"]
    return not any(re.search(pattern, text, re.IGNORECASE) for pattern in unsafe)
