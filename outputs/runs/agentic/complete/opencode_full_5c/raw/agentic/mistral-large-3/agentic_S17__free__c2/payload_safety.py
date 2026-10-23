from typing import List
import re


def check_payload_safety(
    payload: str, unsafe_patterns: List[str] = None
) -> Dict[str, Any]:
    if unsafe_patterns is None:
        unsafe_patterns = [
            r"<script.*?>.*?</script>",
            r"onerror=",
            r"onload=",
            r"javascript:",
            r"eval\(",
            r"document\.cookie",
            r"window\.location",
        ]

    findings = []
    for pattern in unsafe_patterns:
        if re.search(pattern, payload, re.IGNORECASE):
            findings.append({"pattern": pattern, "matched": True})
        else:
            findings.append({"pattern": pattern, "matched": False})

    return {
        "payload_safe": not any(finding["matched"] for finding in findings),
        "findings": findings,
    }
