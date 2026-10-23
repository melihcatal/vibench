import json
from vision_client import VisionClient
from vision_models import Normalizer


def summarize_visual_analysis(
    labels: list, description: str, texts: list, safety: bool
) -> dict:
    """Summarizes results from the same-scenario image analysis steps.

    Returns a dict with combined findings suitable for downstream pipelines.
    """
    summary = {
        "labels": labels,
        "description": description,
        "extracted_text": texts,
        "safe": safety,
        "summary": f"The image contains {', '.join(labels)} and the visual description is: '{description}'. \nExtracted text: {', '.join(texts) if texts else 'None detected'}. \nSafety check: {'SAFE' if safety else 'UNSAFE'}",
    }
    return summary
