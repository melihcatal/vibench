# vision_models.py
import json
import uuid
from typing import List, Dict

def normalize_labels(labels: List[str]) -> List[str]:
    """Lowercase and deduplicate labels."""
    return sorted({lbl.lower().strip() for lbl in labels})

def normalize_description(text: str) -> str:
    """Trim whitespace and add ellipsis if long."""
    txt = text.strip()
    return txt if len(txt) <= 200 else txt[:197] + \"...\"

def normalize_text(full_text: str) -> str:
    """Remove extraneous newlines and whitespace."""
    return \" \".join(full_text.strip().split())

def normalize_safecheck(result: bool) -> bool:
    return result
