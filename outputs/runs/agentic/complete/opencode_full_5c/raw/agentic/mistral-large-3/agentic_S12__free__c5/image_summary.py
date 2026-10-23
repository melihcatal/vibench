from typing import List, Dict, Optional
from vision_models import (
    ImageLabel,
    ImageTextDetection,
    ImageDescription,
    ImageSafetyRating,
)


def summarize_visual_analysis(
    labels: List[ImageLabel],
    text_detections: List[ImageTextDetection],
    description: Optional[ImageDescription],
    safety_ratings: List[ImageSafetyRating],
) -> Dict:
    """Summarizes visual analysis results into a structured report."""
    summary = {
        "labels": [
            {"description": label.description, "score": label.score} for label in labels
        ],
        "text_detections": [{"text": text.text} for text in text_detections],
        "description": description.description
        if description
        else "No description generated.",
        "safety_ratings": [
            {"category": rating.category, "probability": rating.probability}
            for rating in safety_ratings
        ],
    }

    return summary
