# LATER-STEP
import re
from observability_models import DimensionFilter

def metric_annotation_safety(annotation: str) -> bool:
    """Check free-text metric labels or annotations for unsafe text.

    Returns True if safe (no disallowed patterns), False otherwise.
    """
    # Example unsafe patterns: SQL keywords, JavaScript execution, command injection
    unsafe_patterns = [
        r'(?i)drop\s+table',
        r'(?i)exec\s+.*\\(', 
        r'(?i)union\s+select',
        r'(?i)drop\s+database',
        r'(?i)insert\s+into',
        r'(?i)delete\s+from',
        r'(?i);\\s*',   # trailing semicolon
        r'(?i)\\bjavascript:\\b',
        r'(?i)\\bon\\w+=',
    ]
    for pattern in unsafe_patterns:
        if re.search(pattern, annotation):
            return False
    return True
