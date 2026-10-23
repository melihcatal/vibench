from __future__ import annotations

from typing import Iterable

from openai import OpenAI

from vision_models import DescriptionResult, LabelResult, TextDetectionResult


client = OpenAI()
MODEL_ID = "gpt-4o-mini"


def summarize_visual_analysis(labels: Iterable[LabelResult], description: DescriptionResult, text: Iterable[TextDetectionResult]) -> str:
    label_text = ", ".join(label.name for label in labels)
    ocr_text = " ".join(item.text for item in text)
    prompt = (
        f"Labels: {label_text}\n"
        f"Description: {description.description}\n"
        f"Detected text: {ocr_text}\n"
        "Write one concise summary of the image analysis."
    )
    response = client.chat.completions.create(
        model=MODEL_ID,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    return response.choices[0].message.content or ""
