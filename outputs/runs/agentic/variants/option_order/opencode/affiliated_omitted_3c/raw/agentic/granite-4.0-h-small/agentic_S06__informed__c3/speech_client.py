import os
from typing import Any, Dict
from dashscope import Tts


class SpeechClient:
    """Local helper class to encapsulate Text-to-Speech configuration and helper utilities.

    Uses DashScope CosyVoice TTS as the concrete provider.
    """

    def __init__(self, api_key: str | None = None):
        # Prefer environment variable; fallback to passed argument
        self.api_key = api_key or os.getenv("DASHSCOPE_API_KEY")
        if not self.api_key:
            raise ValueError(
                "DASHSCOPE_API_KEY must be set in environment or passed to constructor"
            )
        self.client = Tts(api_key=self.api_key)

    def synth_text(
        self, text: str, voice: str, locale: str, format: str = "wav"
    ) -> bytes | None:
        """Synthesize plain text to audio bytes."""
        payload = {
            "text": text,
            "format": format,
            "voice": voice,
            "params": {"sampling_rate": 24000},
        }
        try:
            response = self.client.tts(text=payload)
            return response.get("audio")
        except Exception as exc:
            print(f"Synthesis error: {exc}")
            return None

    def synth_ssml(
        self, ssml: str, voice: str, locale: str, format: str = "wav"
    ) -> bytes | None:
        """Synthesize SSML to audio bytes."""
        payload = {
            "text": ssml,
            "format": format,
            "voice": voice,
            "params": {"sampling_rate": 24000},
        }
        try:
            response = self.client.tts(text=payload)
            return response.get("audio")
        except Exception as exc:
            print(f"SSML synthesis error: {exc}")
            return None

    def list_voices(self, locale: str) -> list[Dict[str, Any]]:
        """Retrieve voice catalog for locale."""
        payload = {"locale": locale}
        try:
            response = self.client.metadata_voices(payload)
            return response.get("voices", [])
        except Exception as exc:
            print(f"Error fetching voices: {exc}")
            return []
