from __future__ import annotations

from detect_image_labels import detect_image_labels
from detect_image_text import detect_image_text
from vision_client import openai_client, to_openai_input_text
from vision_models import ImageDescriptionResult


def describe_image(image: str) -> dict:
    labels = detect_image_labels(image)
    text = detect_image_text(image)
    client = openai_client()
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        temperature=0.2,
        messages=[
            {
                "role": "system",
                "content": "Write one short, realistic visual description using detected labels and visible text.",
            },
            {
                "role": "user",
                "content": to_openai_input_text(
                    {"labels": labels.get("labels", []), "text": text.get("text", "")}
                ),
            },
        ],
    )
    description = response.choices[0].message.content or ""
    result = ImageDescriptionResult(
        provider="openai",
        description=description.strip(),
        raw_response=response.model_dump(),
    )
    return result.to_dict()
