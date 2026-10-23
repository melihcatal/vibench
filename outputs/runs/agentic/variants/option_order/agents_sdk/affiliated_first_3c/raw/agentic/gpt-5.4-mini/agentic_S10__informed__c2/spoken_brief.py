from __future__ import annotations

import os
from pathlib import Path

import requests

from model_client import DEFAULT_OPENAI_MODEL, LLMRequest, chat_completion
from model_models import SpokenBriefResult

ELEVENLABS_API_URL = "https://api.elevenlabs.io/v1/text-to-speech"


def generate_spoken_brief(text: str, voice_id: str, model: str = DEFAULT_OPENAI_MODEL, output_path: str = "spoken_brief.mp3") -> SpokenBriefResult:
    script = chat_completion(
        LLMRequest(
            model=model,
            messages=[
                {"role": "system", "content": "Write a brief, spoken-style version of the input text."},
                {"role": "user", "content": text},
            ],
            temperature=0.4,
            max_tokens=220,
        )
    ).text
    api_key = os.getenv("ELEVENLABS_API_KEY")
    response = requests.post(
        f"{ELEVENLABS_API_URL}/{voice_id}",
        headers={"xi-api-key": api_key, "Content-Type": "application/json"},
        json={"text": script, "model_id": "eleven_multilingual_v2"},
        timeout=60,
    )
    Path(output_path).write_bytes(response.content)
    return SpokenBriefResult(audio_path=output_path, text=script, raw=response)
