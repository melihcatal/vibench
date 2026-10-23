# image_summary.py
"""Summarize visual analysis results from the same‑scenario helpers.

Combines labels, descriptions, detected text and safety scores into a single concise
summary object that can be stored, displayed or further processed."

import json
from typing import Dict, List
from vision_models import normalize_labels, normalize_description, normalize_text, normalize_safety

def summarize(image_path: str) -> Dict[str, Any]:
    """Orchestrates same‑scenario steps and returns a unified summary."""
    # 1. Detect labels
    labels_raw = VisionClient().label_image(image_path)
    labels = normalize_labels(labels_raw)

    # 2. Generate description
    desc_raw = VisionClient().describe(image_path)
    description = normalize_description(desc_raw)

    # 3. Detect text inside image
    text_raw = VisionClient().detect_text(image_path)
    text_lines = normalize_text(text_raw)

    # 4. Safety check
    safety_raw = VisionClient().safety_check(image_path)
    safety = normalize_safety(safety_raw)

    # Assemble summary
    summary = {
        "image_path": image_path,
        "labels": labels,
        "description": description,
        "text": text_lines,
        "safety": safety
    }
    return summary
