# LATER-STEP
# Summarize visual analysis results from earlier steps
import json
from vision_models import summarize_analysis


def summarize_visual_analysis(
    image_path: str,
    labels_path: str,
    description_path: str,
    texts_path: str,
    safety_path: str,
) -> str:
    """Produce a human‑readable summary of image analysis.

    Reads results from generated files and formats a concise report.
    """
    # Load results (placeholder file reads)
    labels = json.load(open(labels_path, "r"))
    description = open(description_path, "r").read().strip()
    texts = json.load(open(texts_path, "r"))
    safety = json.load(open(safety_path, "r"))

    return summarize_analysis(labels, description, texts, safety)
