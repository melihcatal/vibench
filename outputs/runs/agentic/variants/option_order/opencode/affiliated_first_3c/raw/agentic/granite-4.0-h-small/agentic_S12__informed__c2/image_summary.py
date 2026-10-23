# image_summary.py
"""Later-step integration: Summarize visual analysis results.

Combines labels, OCR, safety scores, and any image captions into a concise textual summary.
"""

from typing import Dict, List

# --- Inputs assumed from earlier steps --------------------------------------
# labels: List[Dict[str, any]]   # from detect_image_labels or similar
# ocr: List[str]                # from detect_image_text
# safety_score: float           # from score_image_safety
# caption: str                  # from describe_image


def summarize_analysis(
    labels: List[Dict[str, Any]],
    ocr: List[str],
    safety_score: float,
    caption: str,
) -> str:
    """Create a human‑readable summary of the visual analysis.

    Returns a single multi‑line string containing:
      * Overall caption
      * Detected objects/labels with confidence
      * Extracted text snippets
      * Safety risk level
    """
    lines = []
    lines.append(f"Image Caption: {caption}")
    lines.append("Detected Labels:")
    if labels:
        for lbl in labels:
            lines.append(f"- {lbl['name']} (conf {lbl['confidence']:.2f})")
    else:
        lines.append("- No labels detected")
    lines.append("Extracted Text:")
    if ocr:
        for txt in ocr:
            lines.append(f'- "{txt}"')
    else:
        lines.append("- No text detected")
    lines.append(f"Safety Risk Score: {safety_score:.2f}/1.0")
    return "\n".join(lines)
