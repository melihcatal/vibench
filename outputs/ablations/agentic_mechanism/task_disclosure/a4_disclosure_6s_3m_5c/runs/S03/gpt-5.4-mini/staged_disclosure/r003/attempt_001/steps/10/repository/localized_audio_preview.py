import argparse
import base64
import os
from dataclasses import dataclass
from typing import Optional

import requests


@dataclass
class ElevenLabsConfig:
    api_key: str
    voice_id: str
    model_id: str = "eleven_multilingual_v2"
    endpoint: str = "https://api.elevenlabs.io/v1/text-to-speech"
    timeout: float = 60.0


def load_config() -> ElevenLabsConfig:
    api_key = os.getenv("ELEVENLABS_API_KEY", "")
    voice_id = os.getenv("ELEVENLABS_VOICE_ID", "")
    if not api_key:
        raise RuntimeError("ELEVENLABS_API_KEY is required")
    if not voice_id:
        raise RuntimeError("ELEVENLABS_VOICE_ID is required")
    return ElevenLabsConfig(
        api_key=api_key,
        voice_id=voice_id,
        model_id=os.getenv("ELEVENLABS_MODEL_ID", "eleven_multilingual_v2"),
        endpoint=os.getenv("ELEVENLABS_ENDPOINT", "https://api.elevenlabs.io/v1/text-to-speech"),
        timeout=float(os.getenv("ELEVENLABS_TIMEOUT", "60")),
    )


def synthesize_preview(text: str, output_path: str, language_code: Optional[str] = None) -> str:
    config = load_config()
    payload = {
        "text": text,
        "model_id": config.model_id,
        "voice_settings": {
            "stability": float(os.getenv("ELEVENLABS_STABILITY", "0.5")),
            "similarity_boost": float(os.getenv("ELEVENLABS_SIMILARITY_BOOST", "0.75")),
        },
    }
    if language_code:
        payload["language_code"] = language_code
    response = requests.post(
        f"{config.endpoint.rstrip('/')}/{config.voice_id}",
        headers={
            "xi-api-key": config.api_key,
            "Content-Type": "application/json",
            "Accept": "audio/mpeg",
        },
        json=payload,
        timeout=config.timeout,
    )
    response.raise_for_status()
    with open(output_path, "wb") as f:
        f.write(response.content)
    return output_path


def preview_from_base64(text: str, language_code: Optional[str] = None) -> str:
    config = load_config()
    payload = {
        "text": text,
        "model_id": config.model_id,
        "voice_settings": {
            "stability": float(os.getenv("ELEVENLABS_STABILITY", "0.5")),
            "similarity_boost": float(os.getenv("ELEVENLABS_SIMILARITY_BOOST", "0.75")),
        },
    }
    if language_code:
        payload["language_code"] = language_code
    response = requests.post(
        f"{config.endpoint.rstrip('/')}/{config.voice_id}",
        headers={
            "xi-api-key": config.api_key,
            "Content-Type": "application/json",
            "Accept": "audio/mpeg",
        },
        json=payload,
        timeout=config.timeout,
    )
    response.raise_for_status()
    return base64.b64encode(response.content).decode("ascii")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate spoken previews of translated copy using ElevenLabs.")
    parser.add_argument("text")
    parser.add_argument("output_path")
    parser.add_argument("--language-code", default=None)
    args = parser.parse_args()
    synthesize_preview(args.text, args.output_path, args.language_code)


if __name__ == "__main__":
    main()
