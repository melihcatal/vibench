import os
from vision_models import ImageAnalysis


def summarize_analysis(analysis: ImageAnalysis) -> dict:
    """Create a concise summary from the full analysis object.
    Returns a dict with key fields:
        - label_count: number of distinct labels
        - description: the generated caption
        - ocr_count: total words detected
        - safe: safety verdict
    """
    summary = {
        "label_count": len(analysis.labels),
        "description": analysis.description,
        "ocr_word_count": sum(len(line.words) for line in analysis.ocr),
        "safe": analysis.safe,
    }
    return summary
