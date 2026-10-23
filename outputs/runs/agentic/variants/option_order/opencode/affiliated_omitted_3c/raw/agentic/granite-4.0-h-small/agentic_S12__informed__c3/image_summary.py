# image_summary.py
import json
import os
from vision_models import shorten_description, is_unsafe


def summarize_analysis(image_path, labels, description, ocr_texts, safe):
    """Create a JSON summary of image analysis results."""
    summary = {
        "image_path": image_path,
        "labels": labels,
        "description": shorten_description(description),
        "ocr": ocr_texts,
        "safe": not safe,
        "unsafe_categories": [cat for cat, value in safe.items() if value],
    }
    output_path = os.path.splitext(image_path)[0] + "_summary.json"
    with open(output_path, "w") as f:
        json.dump(summary, f, indent=2)
    return output_path
