from __future__ import annotations

from openai import OpenAI

from vision_client import to_openai_input_text
from vision_models import ImageSummaryResult, compact_analysis_payload


def image_summary(
    label_result: dict, description_result: dict, text_result: dict, safety_result: dict
) -> dict:
    payload = compact_analysis_payload(
        {
            "labels": label_result.get("labels"),
            "description": description_result.get("description"),
            "text": text_result.get("text"),
            "safety": {
                "safe": safety_result.get("safe"),
                "categories": safety_result.get("categories"),
            },
        }
    )
    client = OpenAI(api_key=__import__("os").getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        temperature=0.2,
        messages=[
            {
                "role": "system",
                "content": "Summarize image analysis results in 2 concise sentences.",
            },
            {"role": "user", "content": to_openai_input_text(payload)},
        ],
    )
    result = ImageSummaryResult(
        provider="openai",
        summary=(response.choices[0].message.content or "").strip(),
        raw_response=response.model_dump(),
    )
    return result.to_dict()
