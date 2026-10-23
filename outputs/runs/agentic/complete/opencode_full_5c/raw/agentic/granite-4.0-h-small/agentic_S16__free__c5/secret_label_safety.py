import re
from typing import List
from security_models import SecretEntry, SecretAuditResult

# Unsafe phrases list (could be loaded from config)
UNSAFE_PHRASES = [
    r"password",
    r"secret",
    r"key",
    r"credential",
    r"token",
]

# Regex patterns for fast checking
PATTERNS = [re.compile(p, re.IGNORECASE) for p in UNSAFE_PHRASES]


# Check a single secret's label/note for unsafe text
def secret_label_safety(entry: SecretEntry) -> SecretAuditResult:
    """Return safety status and optional issue message."""
    description = entry.get("description", "")
    # Scan description and label together
    full_text = f"{entry.get('label', '')} {description}"
    safe = all(not pat.search(full_text) for pat in PATTERNS)
    issue = entry.get("label") if not safe else None
    return {"entry": entry, "is_safe": safe, "issue": issue}


# Batch helper for many secrets
def batch_check(entries: List[SecretEntry]) -> List[SecretAuditResult]:
    return [secret_label_safety(e) for e in entries]


# Demo (will be removed in production)
if __name__ == "__main__":
    sample = [
        {
            "name": "prod-api",
            "label": "production",
            "description": "this secret contains no unsafe words",
        },
        {
            "name": "test-creds",
            "label": "test",
            "description": "password still in description",
        },
    ]
    print(batch_check(sample))
