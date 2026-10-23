from typing import Optional

from deepgram import DeepgramClient
from openai import OpenAI

from speech_client import load_speech_config
from speech_models import normalize_text


class LiveCaptionTranslator:
    def __init__(self, target_language: str = "es") -> None:
        self.target_language = target_language
        self._openai = OpenAI()

    def translate(self, caption_text: str) -> str:
        text = normalize_text(caption_text)
        if not text:
            return ""
        response = self._openai.responses.create(
            model="gpt-4o-mini",
            input=[
                {
                    "role": "system",
                    "content": f"Translate live captions into {self.target_language}. Keep meaning concise.",
                },
                {"role": "user", "content": text},
            ],
        )
        return normalize_text(response.output_text)

