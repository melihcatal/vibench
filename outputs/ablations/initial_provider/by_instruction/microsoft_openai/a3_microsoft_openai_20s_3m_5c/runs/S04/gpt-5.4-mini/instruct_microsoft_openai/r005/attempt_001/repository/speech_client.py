import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests


@dataclass
class SpeechClientConfig:
    openai_api_key: str
    openai_base_url: str = "https://api.openai.com/v1"
    openai_transcription_model: str = "gpt-4o-mini-transcribe"
    openai_reasoning_model: str = "gpt-4.1-mini"


def load_speech_config() -> SpeechClientConfig:
    return SpeechClientConfig(
        openai_api_key=os.environ["OPENAI_API_KEY"],
        openai_base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"),
        openai_transcription_model=os.getenv("OPENAI_TRANSCRIPTION_MODEL", "gpt-4o-mini-transcribe"),
        openai_reasoning_model=os.getenv("OPENAI_REASONING_MODEL", "gpt-4.1-mini"),
    )


class OpenAIHttpClient:
    def __init__(self, config: Optional[SpeechClientConfig] = None):
        self.config = config or load_speech_config()
        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Bearer {self.config.openai_api_key}"})

    def post(self, path: str, *, json: Optional[Dict[str, Any]] = None, files: Optional[Dict[str, Any]] = None):
        return self.session.post(f"{self.config.openai_base_url}{path}", json=json, files=files, timeout=120)

    def get(self, path: str, *, params: Optional[Dict[str, Any]] = None):
        return self.session.get(f"{self.config.openai_base_url}{path}", params=params, timeout=120)
