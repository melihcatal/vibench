import re
from typing import Dict, List


def check_secret_labels(secret_metadata: Dict[str, str]) -> Dict[str, List[str]]:
    unsafe_patterns = [
        r"password",
        r"secret",
        r"key",
        r"token",
        r"credential",
        r"admin",
        r"root",
        r"prod",
        r"dev",
        r"test",
    ]

    results = {}

    for field, value in secret_metadata.items():
        if not isinstance(value, str):
            continue

        unsafe_findings = []
        for pattern in unsafe_patterns:
            if re.search(pattern, value, re.IGNORECASE):
                unsafe_findings.append(pattern)

        if unsafe_findings:
            results[field] = unsafe_findings

    return results


def secret_label_safety(
    secret_id: str, labels: Dict[str, str], notes: str
) -> Dict[str, Dict[str, List[str]]]:
    metadata = {**labels, "notes": notes}

    unsafe_labels = check_secret_labels(labels)
    unsafe_notes = check_secret_labels({"notes": notes})

    return {"secret_id": {"unsafe_labels": unsafe_labels}, "notes": unsafe_notes}
