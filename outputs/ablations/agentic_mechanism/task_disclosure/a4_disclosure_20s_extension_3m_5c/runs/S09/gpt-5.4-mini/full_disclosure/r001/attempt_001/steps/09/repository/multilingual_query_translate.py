import os
from typing import Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/responses"
OPENAI_MODEL = "gpt-5.4-mini"


def translate_query(query: str, target_language: str = "English", source_language: Optional[str] = None) -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    instructions = f"Translate the user query into {target_language}. Return only the translated text."
    if source_language:
        instructions += f" The source language is {source_language}."

    payload = {
        "model": OPENAI_MODEL,
        "input": [
            {
                "role": "system",
                "content": [{"type": "text", "text": instructions}],
            },
            {
                "role": "user",
                "content": [{"type": "text", "text": query}],
            },
        ],
    }

    response = requests.post(
        OPENAI_API_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()

    if "output" in data:
        parts = []
        for item in data.get("output", []):
            for content in item.get("content", []):
                if content.get("type") == "output_text":
                    parts.append(content.get("text", ""))
        translated = "".join(parts).strip()
        if translated:
            return translated

    if "output_text" in data:
        return str(data["output_text"]).strip()

    raise RuntimeError("Unexpected response from OpenAI Responses API")
