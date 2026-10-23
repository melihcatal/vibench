from typing import Dict, Any
from vision_models import VisualAnalysisSummary

def image_summary(
    labels: Dict[str, Any],
    description: Dict[str, Any],
    detected_text: Dict[str, Any],
    safety: Dict[str, Any]
) -> VisualAnalysisSummary:
    """Summarizes visual analysis results from prior steps."""
    return VisualAnalysisSummary(
        labels=labels.get("labels", []),
        description=description.get("description", ""),
        detected_text=detected_text.get("full_text", ""),
        safety_issues={
            "adult": safety.get("adult", "UNKNOWN"),
            "violence": safety.get("violence", "UNKNOWN"),
            "racy": safety.get("racy", "UNKNOWN"),
            "medical": safety.get("medical", "UNKNOWN"),
            "spoof": safety.get("spoof", "UNKNOWN"),
        }
    )