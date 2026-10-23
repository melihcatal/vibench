from __future__ import annotations

import os

import requests


OPENAI_RESPONSES_URL = "https://api.openai.com/v1/responses"
OPENAI_API_KEY_ENV = "OPENAI_API_KEY"
OPENAI_AUDIO_MODEL = "gpt-4o-mini-tts"
OPENAI_TEXT_MODEL = "gpt-4.1-mini"
OPENAI_VOICE = "alloy"


def generate_audio_brief(retrieved_results: list[dict[str, str]]) -> dict[str, str]:
    api_key = os.environ[OPENAI_API_KEY_ENV]
    summary_text = " ".join(
        item.get("text", "") for item in retrieved_results[:5]
    ).strip()
    response = requests.post(
        OPENAI_RESPONSES_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": OPENAI_TEXT_MODEL,
            "input": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_text",
                            "text": f"Create a concise spoken brief from these retrieval results: {summary_text}",
                        }
                    ],
                }
            ],
            "text": {"format": {"type": "text"}},
            "audio": {"voice": OPENAI_VOICE, "format": "mp3"},
        },
        timeout=60,
    )
    response.raise_for_status()
    payload = response.json()
    output_text = payload.get("output", [{}])[0].get("content", [{}])[0].get("text", "")
    return {
        "provider": "OpenAI",
        "text_model": OPENAI_TEXT_MODEL,
        "audio_model_family": OPENAI_AUDIO_MODEL,
        "voice": OPENAI_VOICE,
        "brief_text": output_text,
    }
