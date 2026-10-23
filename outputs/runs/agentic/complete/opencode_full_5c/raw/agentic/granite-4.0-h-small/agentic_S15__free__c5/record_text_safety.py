# record_text_safety.py
# Later-step: Check user-generated document fields for unsafe content
import re
from typing import Dict


def scan_inappropriate_text(record: Dict[str, str]) -> bool:
    """Scan a document's textual fields for disallowed patterns.

    Currently flags any occurrence of the word \"unsafe\" (case-insensitive).
    Replace this mock logic with a real moderation service if needed.
    """
    text_fields = [v for v in record.values() if isinstance(v, str)]
    pattern = re.compile(r"unsafe", re.IGNORECASE)
    return any(pattern.search(field) for field in text_fields)
