from google.cloud import translate_v2 as translate
from typing import List, Optional, Dict, Any
import asyncio


class LiveCaptionTranslator:
    def __init__(self, target_language: str = "es", project_id: Optional[str] = None):
        self.client = translate.Client()
        self.target_language = target_language
        self.project_id = project_id

    def translate_text(
        self, text: str, source_language: Optional[str] = None
    ) -> Dict[str, Any]:
        if source_language:
            result = self.client.translate(
                text,
                target_language=self.target_language,
                source_language=source_language,
                format_="text",
            )
        else:
            result = self.client.translate(
                text, target_language=self.target_language, format_="text"
            )

        return {
            "translated_text": result["translatedText"],
            "source_language": result.get("detectedSourceLanguage", source_language),
            "original_text": text,
        }

    def translate_caption(self, caption: str, is_final: bool = True) -> Dict[str, Any]:
        translation = self.translate_text(caption)
        return {
            **translation,
            "is_final": is_final,
            "target_language": self.target_language,
        }

    async def translate_stream(self, caption_stream):
        async for caption, is_final in caption_stream:
            translation = self.translate_caption(caption, is_final)
            yield translation

    def batch_translate(self, captions: List[str]) -> List[Dict[str, Any]]:
        if not captions:
            return []

        results = self.client.translate(
            captions, target_language=self.target_language, format_="text"
        )

        translations = []
        for i, result in enumerate(results):
            translations.append(
                {
                    "translated_text": result["translatedText"],
                    "source_language": result.get("detectedSourceLanguage"),
                    "original_text": captions[i],
                }
            )

        return translations

    def get_supported_languages(self) -> List[Dict[str, str]]:
        languages = self.client.get_languages()
        return languages

    def detect_language(self, text: str) -> Dict[str, Any]:
        result = self.client.detect_language(text)
        return {"language": result["language"], "confidence": result["confidence"]}

    def set_target_language(self, language_code: str):
        self.target_language = language_code

    def create_bilingual_caption(self, original: str, translated: str) -> str:
        return f"{original} → {translated}"

    def translate_with_context(
        self, text: str, context: Optional[str] = None
    ) -> Dict[str, Any]:
        if context:
            combined = f"{context} {text}"
            translation = self.translate_text(combined)
            return {**translation, "has_context": True, "context": context}
        else:
            return self.translate_text(text)
