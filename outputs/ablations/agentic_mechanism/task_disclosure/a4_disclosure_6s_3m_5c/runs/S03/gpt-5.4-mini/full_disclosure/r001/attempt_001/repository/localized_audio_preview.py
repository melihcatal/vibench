import os
from typing import List, Dict, Any, Optional

import requests


OPENAI_TTS_URL = "https://api.openai.com/v1/audio/speech"
OPENAI_TTS_MODEL = "gpt-4o-mini-tts"


def generate_spoken_previews(translated_copy: List[str], voice: str = "alloy", output_dir: Optional[str] = None) -> List[Dict[str, Any]]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")

    output_dir = output_dir or os.getcwd()
    previews: List[Dict[str, Any]] = []

    for index, text in enumerate(translated_copy):
        response = requests.post(
            OPENAI_TTS_URL,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": OPENAI_TTS_MODEL,
                "voice": voice,
                "input": text,
                "format": "mp3",
            },
            timeout=60,
        )
        response.raise_for_status()

        file_path = os.path.join(output_dir, f"localized_preview_{index + 1}.mp3")
        with open(file_path, "wb") as audio_file:
            audio_file.write(response.content)

        previews.append({"text": text, "audio_path": file_path})

    return previews
