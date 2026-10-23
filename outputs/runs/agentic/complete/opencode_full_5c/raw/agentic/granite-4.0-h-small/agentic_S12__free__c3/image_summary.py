# image_summary.py
# [LATER-STEP]

from typing import List
from vision_models import LabelResponse, CaptionResponse, SafetyCheckResponse


def summarize(
    labels: List[LabelResponse], caption: CaptionResponse, safety: SafetyCheckResponse
) -> str:
    """Summarize visual analysis results into a concise paragraph."""
    lines = []
    # Add label information
    if labels:
        line = "Detected objects: " + ", ".join(
            l.name for l_resp in labels for l in l_resp.labels
        )
        lines.append(line)
    # Add caption
    if caption.caption:
        lines.append(caption.caption)
    # Add safety notes
    if not safety_adult(safety):
        lines.append("The image contains no adult content.")
    if not safety_violent(safety):
        lines.append("The image appears free of violent content.")
    return "\n".join(lines)


# Helper flags for safety summaries


def safety_adult(resp: SafetyCheckResponse) -> bool:
    return resp.adult in ("UNLIKELY", "POSSIBLE")


def safety_violent(resp: SafetyCheckResponse) -> bool:
    return resp.violence in ("UNLIKELY", "POSSIBLE")
