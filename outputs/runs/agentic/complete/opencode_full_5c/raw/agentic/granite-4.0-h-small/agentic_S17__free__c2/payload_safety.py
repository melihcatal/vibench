# [LATER-STEP] payload_safety.py

import re

# Simple unsafe content detector (demo only)
UNSAFE_PATTERNS = [
    r"(?i)select\\s+.*from",  # SQL injection attempt
    r"\\bxp_\\w+\\b",  # SQL Server extended stored procedure
    r"\\bDROP\\b",  # Destructive SQL command
    r"\\bEXEC\\b",  # Execution command
    r"\\bUNION\\b ALL\\b",  # UNION ALL injection
]


def contains_unsafe_content(text: str) -> bool:
    """Return True if the payload contains patterns that look unsafe."""
    for pattern in UNSAFE_PATTERNS:
        if re.search(pattern, text):
            return True
    return False


# Example usage
if __name__ == "__main__":
    sample = "SELECT * FROM users;"
    print("Unsafe" if contains_unsafe_content(sample) else "Safe")
