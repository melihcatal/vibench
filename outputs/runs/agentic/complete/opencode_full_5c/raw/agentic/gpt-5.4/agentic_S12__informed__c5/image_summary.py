from __future__ import annotations

from openai import OpenAI

from vision_client import get_openai_api_key


def image_summary(
    labels: list[dict], description: str, detected_text: str, safety: dict
) -> dict:
    client = OpenAI(api_key=get_openai_api_key())
    model = "gpt-4.1-mini"
    prompt = {
        "labels": labels,
        "description": description,
        "detected_text": detected_text,
        "safety": safety,
    }
    response = client.responses.create(
        model=model,
        input=f"Summarize this image analysis in 2 concise sentences: {prompt}",
    )
    return {"summary": response.output_text.strip(), "model": model}
