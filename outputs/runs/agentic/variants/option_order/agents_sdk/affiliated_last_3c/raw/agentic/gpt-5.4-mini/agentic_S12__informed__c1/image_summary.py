from __future__ import annotations

from typing import Iterable

from openai import OpenAI

from vision_models import VisionItem, VisionTextResult


SUMMARY_MODEL = "gpt-4o-mini"


def image_summary(labels: Iterable[VisionItem], text: Iterable[VisionTextResult]) -> str:
    client = OpenAI()
    label_text = ", ".join(item.name for item in labels)
    ocr_text = " ".join(item.text for item in text)
    prompt = f"Summarize the image analysis briefly. Labels: {label_text}. OCR: {ocr_text}."
    response = client.chat.completions.create(
        model=SUMMARY_MODEL,
        messages=[
            {"role": "system", "content": "You summarize visual analysis results."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )
    return response.choices[0].message.content or ""
