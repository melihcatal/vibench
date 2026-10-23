from typing import Dict
from .vision_models import ImageSummaryRequest


def image_summary(request: ImageSummaryRequest) -> Dict:
    """Summarizes visual analysis results into a structured report."""
    summary = {
        "provider": "google_cloud_vision",
        "visual_summary": {
            "description": request.description,
            "key_labels": request.labels[:5],
            "detected_texts": request.texts[:3],
            "safety_ratings": request.safety_ratings,
        },
    }
    return summary
