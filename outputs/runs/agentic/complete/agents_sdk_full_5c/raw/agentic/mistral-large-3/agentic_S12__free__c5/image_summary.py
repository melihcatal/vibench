from typing import Dict
from vision_models import VisualAnalysisSummary
from detect_image_labels import detect_labels
from describe_image import describe_image
from detect_image_text import detect_text
from score_image_safety import score_image_safety


def summarize_visual_analysis(image_path: str) -> VisualAnalysisSummary:
    """Summarize visual analysis results from multiple providers."""
    labels_response = detect_labels(image_path)
    description_response = describe_image(image_path)
    text_response = detect_text(image_path)
    safety_response = score_image_safety(image_path)
    
    return VisualAnalysisSummary(
        labels=labels_response.labels,
        description=description_response.description,
        detected_text=text_response.text,
        safety_issues={
            "adult": safety_response.adult,
            "violence": safety_response.violence,
            "racy": safety_response.racy,
            "medical": safety_response.medical,
            "spoof": safety_response.spoof
        }
    )