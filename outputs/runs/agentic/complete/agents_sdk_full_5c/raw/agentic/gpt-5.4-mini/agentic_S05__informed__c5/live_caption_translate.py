from __future__ import annotations

from typing import Iterable

from google.cloud import translate_v3 as translate

from speech_models import TranslationResult, normalize_text


class LiveCaptionTranslator:
    def __init__(self, project_id: str, location: str = "global") -> None:
        self.client = translate.TranslationServiceClient()
        self.parent = f"projects/{project_id}/locations/{location}"

    def translate_chunk(self, text: str, target_language_code: str, source_language_code: str | None = None) -> TranslationResult:
        text = normalize_text(text)
        request = translate.TranslateTextRequest(
            parent=self.parent,
            contents=[text],
            mime_type="text/plain",
            target_language_code=target_language_code,
            source_language_code=source_language_code or "",
        )
        response = self.client.translate_text(request=request)
        translated = response.translations[0].translated_text if response.translations else ""
        return TranslationResult(
            source_text=text,
            translated_text=translated,
            source_language=source_language_code,
            target_language=target_language_code,
            raw={"provider": "google-cloud-translate-v3"},
        )

    def translate_stream(self, chunks: Iterable[str], target_language_code: str) -> Iterable[TranslationResult]:
        for chunk in chunks:
            yield self.translate_chunk(chunk, target_language_code)
