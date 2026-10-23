from typing import Dict
from .vision_models import ImageSummaryRequest


def summarize_visual_analysis(request: ImageSummaryRequest) -> str:
    """Summarizes visual analysis results from multiple detection sources."""
    summary_parts = []

    if request.labels:
        summary_parts.append(f"Detected labels: {', '.join(request.labels)}")

    if request.description:
        summary_parts.append(request.description)

    if request.detected_text:
        summary_parts.append(f"Detected text: {request.detected_text}")

    if request.safety_scores:
        unsafe_categories = [k for k, v in request.safety_scores.items() if v >= 4]
        if unsafe_categories:
            summary_parts.append(
                f"Unsafe content detected in: {', '.join(unsafe_categories)}"
            )

    return (
        ". ".join(summary_parts)
        if summary_parts
        else "No analysis results to summarize."
    )
