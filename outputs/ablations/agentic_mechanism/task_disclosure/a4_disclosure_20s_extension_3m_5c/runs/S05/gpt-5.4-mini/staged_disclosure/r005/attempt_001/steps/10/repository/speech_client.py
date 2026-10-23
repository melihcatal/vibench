import os
from dataclasses import dataclass
from typing import Dict, Optional

import requests

OPENAI_TRANSCRIBE_URL = "https://api.openai.com/v1/audio/transcriptions"
OPENAI_DEFAULT_MODEL = "gpt-4o-mini-transcribe"


@dataclass(frozen=True)
class SpeechConfig:
    api_key: str
    model: str = OPENAI_DEFAULT_MODEL
    base_url: str = OPENAI_TRANSCRIBE_URL
    timeout: int = 60


class SpeechClientError(RuntimeError):
    pass


def load_speech_config(env: Optional[Dict[str, str]] = None) -> SpeechConfig:
    source = os.environ if env is None else env
    api_key = source.get("OPENAI_API_KEY")
    if not api_key:
        raise SpeechClientError("OPENAI_API_KEY is required")
    model = source.get("OPENAI_SPEECH_MODEL", OPENAI_DEFAULT_MODEL)
    base_url = source.get("OPENAI_SPEECH_API_URL", OPENAI_TRANSCRIBE_URL)
    timeout = int(source.get("OPENAI_SPEECH_TIMEOUT", "60"))
    return SpeechConfig(api_key=api_key, model=model, base_url=base_url, timeout=timeout)


class StreamingSpeechClient:
    def __init__(self, config: Optional[SpeechConfig] = None, env: Optional[Dict[str, str]] = None):
        self.config = config or load_speech_config(env)

    def transcribe_file(self, audio_path: str, language: Optional[str] = None, prompt: Optional[str] = None) -> str:
        headers = {"Authorization": f"Bearer {self.config.api_key}"}
        data = {"model": self.config.model}
        if language:
            data["language"] = language
        if prompt:
            data["prompt"] = prompt
        with open(audio_path, "rb") as audio_file:
            files = {"file": audio_file}
            response = requests.post(self.config.base_url, headers=headers, data=data, files=files, timeout=self.config.timeout)
        if response.status_code >= 400:
            raise SpeechClientError(f"Transcription failed: {response.status_code} {response.text}")
        payload = response.json()
        text = payload.get("text")
        if not isinstance(text, str):
            raise SpeechClientError("Unexpected transcription response")
        return text

    def headers(self) -> Dict[str, str]:
        return {"Authorization": f"Bearer {self.config.api_key}"}
