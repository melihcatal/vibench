# Summarize visual analysis results from multiple detectors
import json


def image_summary(label_report: list, description: str, text: str = None):
    """Create a concise summary combining labels, description, and optional OCR text."""
    summary_parts = []
    if label_report:
        summary_parts.append(f"Labels: {', '.join(label_report)}")
    if description:
        summary_parts.append(f"Description: {description}")
    if text:
        summary_parts.append(
            f"Detected Text: {text[:100]}"
            if len(text) > 100
            else f"Detected Text: {text}"
        )
    return "; ".join(summary_parts)
