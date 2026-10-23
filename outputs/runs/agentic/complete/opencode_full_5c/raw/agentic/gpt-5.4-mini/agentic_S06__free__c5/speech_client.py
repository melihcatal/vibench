import os
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional

import requests

from speech_models import SpeechRequest, SpeechResponse, normalize_ssml


@dataclass
class SpeechClientConfig:
    api_key: str
    region: str = "eastus"
    base_url: str = "https://{region}.tts.speech.microsoft.com/cognitiveservices/v1"
    language: str = "en-US"

    @classmethod
    def from_env(cls) -> "SpeechClientConfig":
        api_key = os.getenv("AZURE_SPEECH_KEY") or os.getenv("SPEECH_KEY") or ""
        region = os.getenv("AZURE_SPEECH_REGION") or os.getenv("SPEECH_REGION") or "eastus"
        language = os.getenv("TTS_LANGUAGE") or "en-US"
        return cls(api_key=api_key, region=region, language=language)

    def resolved_url(self) -> str:
        return self.base_url.format(region=self.region)


class SpeechClient:
    def __init__(self, config: Optional[SpeechClientConfig] = None):
        self.config = config or SpeechClientConfig.from_env()
        self.session = requests.Session()

    def _headers(self, content_type: str = "application/ssml+xml") -> Dict[str, str]:
        headers = {
            "Ocp-Apim-Subscription-Key": self.config.api_key,
            "Content-Type": content_type,
            "User-Agent": "tts-integrations/1.0",
            "X-Microsoft-OutputFormat": "audio-16khz-128kbitrate-mono-mp3",
        }
        return {k: v for k, v in headers.items() if v}

    def synthesize(self, request: SpeechRequest) -> SpeechResponse:
        payload = request.normalized()
        text = payload["text"]
        body = text if not payload.get("ssml") else normalize_ssml(text, payload.get("voice"))
        response = self.session.post(self.config.resolved_url(), data=body.encode("utf-8"), headers=self._headers())
        response.raise_for_status()
        return SpeechResponse(audio=response.content, content_type=response.headers.get("Content-Type", "audio/mpeg"), voice=payload.get("voice"), metadata={"locale": payload.get("locale")})

    def list_voices(self, locale: Optional[str] = None) -> List[Dict[str, Any]]:
        url = f"https://{self.config.region}.tts.speech.microsoft.com/cognitiveservices/voices/list"
        response = self.session.get(url, headers={"Ocp-Apim-Subscription-Key": self.config.api_key})
        response.raise_for_status()
        voices = response.json()
        if locale:
            voices = [voice for voice in voices if voice.get("Locale") == locale]
        return voices

    def select_voice(self, locale: str, preferred: Optional[str] = None) -> Dict[str, Any]:
        voices = self.list_voices(locale)
        if preferred:
            for voice in voices:
                if preferred.lower() in str(voice.get("ShortName", "")).lower():
                    return voice
        return voices[0] if voices else {}

    def save_audio(self, audio: bytes, destination: Any) -> Any:
        if hasattr(destination, "write"):
            destination.write(audio)
            return destination
        with open(destination, "wb") as handle:
            handle.write(audio)
        return destination
