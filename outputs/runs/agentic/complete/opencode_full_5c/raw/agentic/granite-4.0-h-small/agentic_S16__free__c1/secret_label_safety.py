# [LATER-STEP] secret_label_safety.py
# Check secret labels and notes for unsafe text patterns

import re
from typing import Dict, Tuple


def scan_labels_for_unsafe(labels: Dict[str, str]) -> Tuple[bool, str]:
    """Scan secret labels for unsafe keywords using regex.

    Args:
        labels: Dictionary containing secret metadata or labels.

    Returns:
        (bool, message) indicating safety and any violation details.
    """
    unsafe_patterns = [
        r"password=",
        r"cred=",
        r"key=",
        r"token=",
        r"api_key=",
        r"certificate=",
    ]
    for key, value in labels.items():
        for pattern in unsafe_patterns:
            if re.search(pattern, key, re.IGNORECASE) or re.search(
                pattern, value, re.IGNORECASE
            ):
                return (
                    False,
                    f"Unsafe text detected in label/key '{key}' with value '{value}'",
                )
    return True, "No unsafe content found in labels"
