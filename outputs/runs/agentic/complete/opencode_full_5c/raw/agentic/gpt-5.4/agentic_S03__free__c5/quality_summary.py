from __future__ import annotations

import os

import requests

from translation_client import OPENAI_RESPONSES_ENDPOINT, openai_headers


def quality_summary(
    source_text: str, translated_text: str, source_language: str, target_language: str
) -> str:
    response = requests.post(
        OPENAI_RESPONSES_ENDPOINT,
        headers=openai_headers(os.environ.get("OPENAI_API_KEY")),
        json={
            "model": "gpt-5.4",
            "input": [
                {
                    "role": "system",
                    "content": [
                        {
                            "type": "input_text",
                            "text": "Summarize translation quality issues in one concise paragraph.",
                        }
                    ],
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_text",
                            "text": f"Source language: {source_language}\nTarget language: {target_language}\nSource text: {source_text}\nTranslated text: {translated_text}",
                        }
                    ],
                },
            ],
        },
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    return data["output"][0]["content"][0]["text"].strip()
