import re
from typing import List

def detect_unsafe_content(text: str) -> bool:
    """Check selected log message text for unsafe content (e.g., profanity, PII, malicious code).
    Returns True if unsafe patterns are found.
    """
    unsafe_patterns = [
        r"password=\\w+",  # PII - password exposure
        r"(admin|root)\\s+\\w+",  # potential credential leak
        r"(fuck|shit|asshole)",  # profanity (case-insensitive)
        r"(eval\\(|exec\\()",  # potentially dangerous code execution
    ]
    for pat in unsafe_patterns:
        if re.search(pat, text, flags=re.IGNORECASE):
            return True
    return False


def filter_unsafe_logs(logs: List[Dict]) -> List[Dict]:
    """Return a list of logs whose text does NOT contain unsafe content."""
    return [log for log in logs if not detect_unsafe_content(str(log.get("message", "")))]

# Example usage (will be removed in production)
if __name__ == "__main__":
    sample_logs = [
        {"message": "User login successful"},
        {"message": "password=secret"},
        {"message": "This is a fuck-up"},
        {"message": "import os; os.system('rm -rf /')"}
    ]
    safe = filter_unsafe_logs(sample_logs)
    print("Safe logs count:", len(safe))
    for log in safe:
        print(log)
