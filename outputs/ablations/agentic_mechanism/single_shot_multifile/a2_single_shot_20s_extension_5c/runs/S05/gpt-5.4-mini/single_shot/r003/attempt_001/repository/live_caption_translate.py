from typing import Optional

from openai import OpenAI

from speech_client import load_speech_config


def translate_live_caption(text: str, target_language: str, source_language: Optional[str] = None) -> str:
    config = load_speech_config()
    client = OpenAI(api_key=config.api_key or None)
    response = client.responses.create(
        model="gpt-4o-mini",
        input=[
            {
                "role": "system",
                "content": "Translate live meeting captions accurately and preserve names and terminology.",
            },
            {
                "role": "user",
                "content": f"Translate from {source_language or 'auto-detected'} to {target_language}: {text}",
            },
        ],
    )
    return response.output_text
