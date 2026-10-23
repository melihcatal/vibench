from __future__ import annotations

from openai import OpenAI

from storage_models import NormalizedText


def summarize_extracted_asset_content(extracted_text: str, model: str = "gpt-4o-mini") -> NormalizedText:
    client = OpenAI()
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "Summarize the extracted asset content concisely."},
            {"role": "user", "content": extracted_text},
        ],
    )
    summary = response.choices[0].message.content or ""
    return NormalizedText(text=summary, source=f"openai:{model}")
