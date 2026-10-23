from typing import Dict, Any
from vision_models import VisualAnalysisSummary


def summarize_visual_analysis(
    labels: Dict[str, Any],
    description: Dict[str, Any],
    text_detection: Dict[str, Any],
    safety_ratings: Dict[str, Any]
) -> VisualAnalysisSummary:
    """Summarize visual analysis results into a structured format."""
    return VisualAnalysisSummary(
        labels=labels.get("labels", []),
        description=description.get("description", ""),
        detected_text=text_detection.get("full_text", ""),
        safety_ratings=safety_ratings.get("safety_ratings", {})
    )