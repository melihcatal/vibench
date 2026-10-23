from __future__ import annotations

from typing import Iterable

from vision_models import ImageLabelResult, OCRResult, SafetyScore


def summarize_image_analysis(labels: ImageLabelResult, ocr: OCRResult, safety: SafetyScore) -> str:
    label_text = ", ".join(label.description for label in labels.labels[:5]) or "no labels"
    text_preview = (ocr.text[:120] + "...") if len(ocr.text) > 120 else ocr.text
    return (
        f"Labels: {label_text}. "
        f"Text: {text_preview or 'no visible text'}. "
        f"Safety: adult={safety.adult}, violence={safety.violence}, racy={safety.racy}."
    )


__all__ = ["summarize_image_analysis"]
