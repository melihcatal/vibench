# image_summary.py
import json
import uuid
from typing import Dict, List
from vision_models import normalize_description, normalize_labels

def summarize(image_path: str, labels: List[str], description: str, text: str) -> Dict:
    """Create a concise JSON summary of visual analysis."""
    return {
        "image_path": image_path,
        "labels": normalize_labels(labels),
        "description": normalize_description(description),
        "extracted_text": text
    }
