# Moderate vendor notes or memo fields extracted from documents

import re
from typing import List


def moderate_text(text: str) -> List[str]:
    """
    Simple safety filter that removes or flags potentially sensitive content.
    Returns a list of safe lines for downstream processing.
    """
    # Example policy: mask credit card patterns, social security numbers
    patterns = [
        r"\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b",  # Visa/ Mastercard
        r"\b\d{3}[- ]?\d{2}[- ]?\d{4}\b",  # SSN style
        r"\b\d{9,10}\b",
    ]
    lines = text.splitlines()
    safe_lines = []
    for line in lines:
        line_clean = line
        for pat in patterns:
            # Replace found matches with [REDACTED]
            line_clean = re.sub(pat, "[REDACTED]", line_clean)
        if line_clean.strip():  # keep non‑empty lines
            safe_lines.append(line_clean)
    return safe_lines
