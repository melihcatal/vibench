import re
from dataclasses import dataclass
from typing import Iterable, List

import boto3

UNSAFE_PATTERNS = [re.compile(pattern, re.IGNORECASE) for pattern in [r"password", r"secret", r"token", r"private\s*key", r"confidential"]]


@dataclass(frozen=True)
class LabelSafetyResult:
    label: str
    note: str
    is_safe: bool
    reasons: List[str]


def check_label_safety(label: str, note: str) -> LabelSafetyResult:
    combined = f"{label} {note}"
    reasons = [pattern.pattern for pattern in UNSAFE_PATTERNS if pattern.search(combined)]
    return LabelSafetyResult(label=label, note=note, is_safe=not reasons, reasons=reasons)


def redact_unsafe_label(label: str) -> str:
    return re.sub(r"(?i)(password|secret|token|private\s*key|confidential)", "[redacted]", label)
