# [LATER-STEP] image_summary.py

import os
from vision_client import VisionClient
from vision_models import VisionResponseNormalization, normalize_vision_response


def summarize_analysis(image_path: str, results: dict) -> str:
    """Summarizes visual analysis results into a concise report.

    The `results` dict should contain keys produced by the same‑scenario same‑scenario helpers:
    - labels: list of detected labels
    - caption: short description
    - texts: list of OCR‑extracted text strings
    - unsafe: list of unsafe categories (if any)
    """
    # Normalise the possibly heterogeneous provider output into our canonical model.
    norm = normalize_vision_response(results)

    lines = [f"Image: {os.path.basename(image_path)}"]

    if norm.labels:
        lines.append("Detected labels:")
        lines.extend(f"  - {lbl.description}" for lbl in norm.labels)

    if norm.captions:
        lines.append("Visual description:")
        lines.append(f"  - {norm.captions[0].text}")

    if norm.texts:
        lines.append("Extracted text:")
        lines.extend(f"  - {txt.description}" for txt in norm.texts)

    if norm.unsafe:
        lines.append("Safety warnings:")
        lines.extend(
            f"  - {cat.category} (score {cat.score:.2f})" for cat in norm.unsafe
        )

    return "\n".join(lines)
