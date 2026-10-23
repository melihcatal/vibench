from __future__ import annotations

from openai import OpenAI

from speech_models import TranslationResult


class LiveCaptionTranslator:
    def __init__(self, model: str = "gpt-4o-mini") -> None:
        self.client = OpenAI()
        self.model = model

    def translate(self, text: str, target_language: str = "es") -> TranslationResult:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You translate live captions accurately and concisely."},
                {"role": "user", "content": f"Translate this caption into {target_language}: {text}"},
            ],
            temperature=0,
        )
        translated = response.choices[0].message.content or ""
        return TranslationResult(
            source_text=text,
            translated_text=translated,
            target_language=target_language,
            raw={"provider": "openai", "model": self.model, "response_id": response.id},
        )
