import os
from typing import Optional

from openai import OpenAI

from speech_models import NormalizedCaption, normalize_transcript_text

TRANSLATION_MODEL = os.getenv("OPENAI_TRANSLATION_MODEL", "gpt-4o-mini")


class LiveCaptionTranslator:
    def __init__(self, api_key: Optional[str] = None) -> None:
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))

    def translate(self, text: str, target_language: str) -> NormalizedCaption:
        clean_text = normalize_transcript_text(text)
        response = self.client.responses.create(
            model=TRANSLATION_MODEL,
            input=[
                {"role": "system", "content": f"Translate live captions into {target_language}. Preserve meaning and keep it concise."},
                {"role": "user", "content": clean_text},
            ],
        )
        translated = normalize_transcript_text(response.output_text)
        return NormalizedCaption(
            source_text=text,
            normalized_text=translated,
            is_final=True,
        )
