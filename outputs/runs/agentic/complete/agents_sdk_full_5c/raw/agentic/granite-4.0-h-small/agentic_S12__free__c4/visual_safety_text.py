# visual_safety_text.py
import json
import uuid
from vision_models import normalize_text
from vision_client import VisionClient

def check_visual_safety_labels(labels: List[str], unsafe_keywords=None) -> bool:
    """Flag if any label contains potentially unsafe language."""
    if unsafe_keywords is None:
        unsafe_keywords = [\"nude\", \"violence\", \"hate\", \"rude\", \"medical\"]
    safe = all(unsafe not in normalize_text(lbl).lower() for lbl in labels for unsafe in unsafe_keywords)
    return safe
