from __future__ import annotations

from openai import OpenAI

from translation_client import get_openai_api_key


def quality_summary(
    source_text: str, translated_text: str, target_language: str
) -> str:
    client = OpenAI(api_key=get_openai_api_key())
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "system",
                "content": "You review translation quality and return a concise issue summary focusing on accuracy, fluency, terminology, and missing content.",
            },
            {
                "role": "user",
                "content": f"Target language: {target_language}\nSource:\n{source_text}\n\nTranslation:\n{translated_text}",
            },
        ],
    )
    return response.output_text
