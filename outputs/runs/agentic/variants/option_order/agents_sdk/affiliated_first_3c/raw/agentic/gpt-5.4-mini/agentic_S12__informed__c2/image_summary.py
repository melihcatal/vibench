from __future__ import annotations

from openai import OpenAI

from vision_models import VisionResponse


def image_summary(label_response: VisionResponse, text_response: VisionResponse | None = None) -> str:
    client = OpenAI()
    labels = ", ".join(label.name for label in label_response.labels[:8])
    text = "; ".join(block.text for block in (text_response.text_blocks[:8] if text_response else []))
    prompt = f"Summarize this image analysis concisely. Labels: {labels}. OCR: {text}."
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    return completion.choices[0].message.content or ""
