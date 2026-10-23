from typing import List, Dict
from vision_client import parse_vision_response
from vision_models import VisionResponse


# Example integration that aggregates results from the same‑scenario helpers
def summarize_visual_analysis(image_path: str) -> Dict[str, Any]:
    """Summarizes the output of label detection, description, text detection, and safety checks."""
    labels = detect_image_labels(image_path)
    description = describe_image(image_path)
    text = detect_image_text(image_path)
    safe = score_image_safety(image_path)
    return {
        "image_path": image_path,
        "labels": labels,
        "description": description,
        "extracted_text": text,
        "safe": safe,
    }


# Export for downstream pipelines
__all__ = ["summarize_visual_analysis"]
