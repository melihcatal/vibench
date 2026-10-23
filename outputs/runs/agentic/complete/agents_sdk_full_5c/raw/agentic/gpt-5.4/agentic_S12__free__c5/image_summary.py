from __future__ import annotations

import os
from typing import Iterable, Sequence

from anthropic import Anthropic

from vision_models import OCRTextBlock, SafetyCategory, VisualDescription


ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-3-5-haiku-20241022")


def image_summary(labels: Sequence[str], description: VisualDescription | None, text_blocks: Iterable[OCRTextBlock], safety: Iterable[SafetyCategory]) -> str:
    client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    ocr_text = "; ".join(block.text for block in text_blocks if block.text.strip())
    safety_line = ", ".join(f"{item.name}:{item.confidence}" for item in safety)
    desc = description.text if description else ""
    prompt = (
        "Summarize these image-analysis results in 2 concise sentences. "
        f"Labels: {', '.join(labels)}. Description: {desc}. OCR: {ocr_text}. Safety: {safety_line}."
    )
    response = client.messages.create(
        model=ANTHROPIC_MODEL,
        max_tokens=140,
        messages=[{"role": "user", "content": prompt}],
    )
    return "".join(block.text for block in response.content if getattr(block, "type", "") == "text").strip()
