from typing import Dict
from vision_models import VisualAnalysisSummary


def summarize_visual_analysis(
    labels: Dict,
    description: Dict,
    detected_text: Dict,
    safety_scores: Dict
) -> VisualAnalysisSummary:
    """Summarizes visual analysis results into a structured format."""
    return VisualAnalysisSummary(
        labels=labels.get("labels", []),
        description=description.get("description", ""),
        detected_text=detected_text.get("text", ""),
        safety_scores=safety_scores.get("safety_scores", {})
    )