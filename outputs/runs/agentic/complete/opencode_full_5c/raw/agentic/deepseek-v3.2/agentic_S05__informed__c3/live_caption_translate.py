import os
import asyncio
from typing import AsyncGenerator, Dict, Any, Optional
import deepl


class LiveCaptionTranslator:
    def __init__(self, source_lang: str = "EN", target_lang: str = "ES"):
        self.api_key = os.environ.get("DEEPL_AUTH_KEY")
        if not self.api_key:
            raise ValueError("DEEPL_AUTH_KEY environment variable must be set")

        self.translator = deepl.Translator(self.api_key)
        self.source_lang = source_lang
        self.target_lang = target_lang

        self.supported_languages = {
            "BG": "Bulgarian",
            "CS": "Czech",
            "DA": "Danish",
            "DE": "German",
            "EL": "Greek",
            "EN": "English",
            "ES": "Spanish",
            "ET": "Estonian",
            "FI": "Finnish",
            "FR": "French",
            "HU": "Hungarian",
            "ID": "Indonesian",
            "IT": "Italian",
            "JA": "Japanese",
            "KO": "Korean",
            "LT": "Lithuanian",
            "LV": "Latvian",
            "NB": "Norwegian",
            "NL": "Dutch",
            "PL": "Polish",
            "PT": "Portuguese",
            "RO": "Romanian",
            "RU": "Russian",
            "SK": "Slovak",
            "SL": "Slovenian",
            "SV": "Swedish",
            "TR": "Turkish",
            "UK": "Ukrainian",
            "ZH": "Chinese",
        }

    async def translate_caption(
        self, caption_text: str, is_final: bool = True
    ) -> Dict[str, Any]:
        if not caption_text.strip():
            return {
                "original": caption_text,
                "translated": "",
                "source_lang": self.source_lang,
                "target_lang": self.target_lang,
                "is_final": is_final,
                "confidence": 0.0,
            }

        try:
            result = self.translator.translate_text(
                caption_text, source_lang=self.source_lang, target_lang=self.target_lang
            )

            return {
                "original": caption_text,
                "translated": result.text,
                "source_lang": result.detected_source_language
                if hasattr(result, "detected_source_language")
                else self.source_lang,
                "target_lang": self.target_lang,
                "is_final": is_final,
                "confidence": 1.0,
                "provider": "DeepL",
            }
        except Exception as e:
            return {
                "original": caption_text,
                "translated": caption_text,
                "source_lang": self.source_lang,
                "target_lang": self.target_lang,
                "is_final": is_final,
                "confidence": 0.0,
                "error": str(e),
                "provider": "DeepL",
            }

    async def stream_translate_captions(
        self, caption_stream: AsyncGenerator[Dict[str, Any], None]
    ) -> AsyncGenerator[Dict[str, Any], None]:
        async for caption in caption_stream:
            caption_text = caption.get("text", "")
            is_final = caption.get("is_final", True)

            translation = await self.translate_caption(caption_text, is_final)

            result = {
                **caption,
                "translation": translation,
                "translated_text": translation["translated"],
                "translation_metadata": {
                    "source_lang": translation["source_lang"],
                    "target_lang": translation["target_lang"],
                    "provider": "DeepL",
                    "confidence": translation["confidence"],
                },
            }

            yield result

    def get_usage(self) -> Dict[str, Any]:
        try:
            usage = self.translator.get_usage()
            return {
                "character_count": usage.character.count,
                "character_limit": usage.character.limit,
                "character_percentage": (
                    usage.character.count / usage.character.limit * 100
                )
                if usage.character.limit > 0
                else 0,
                "document_count": usage.document.count
                if hasattr(usage, "document")
                else 0,
                "document_limit": usage.document.limit
                if hasattr(usage, "document")
                else 0,
            }
        except:
            return {"error": "Unable to fetch usage information"}

    def set_languages(self, source_lang: str, target_lang: str):
        if source_lang.upper() not in self.supported_languages:
            raise ValueError(f"Unsupported source language: {source_lang}")
        if target_lang.upper() not in self.supported_languages:
            raise ValueError(f"Unsupported target language: {target_lang}")

        self.source_lang = source_lang.upper()
        self.target_lang = target_lang.upper()


async def translate_live_captions(
    caption_stream: AsyncGenerator[Dict[str, Any], None],
    target_language: str = "ES",
    source_language: Optional[str] = None,
) -> AsyncGenerator[Dict[str, Any], None]:
    translator = LiveCaptionTranslator(
        source_lang=source_language or "EN", target_lang=target_language
    )

    async for translated in translator.stream_translate_captions(caption_stream):
        yield translated


class MultiLanguageTranslator:
    def __init__(self):
        self.api_key = os.environ.get("DEEPL_AUTH_KEY")
        if not self.api_key:
            raise ValueError("DEEPL_AUTH_KEY environment variable must be set")

        self.translator = deepl.Translator(self.api_key)

    async def translate_to_multiple_languages(
        self, text: str, target_languages: list
    ) -> Dict[str, Dict[str, Any]]:
        results = {}

        for lang in target_languages:
            try:
                result = self.translator.translate_text(text, target_lang=lang)
                results[lang] = {
                    "text": result.text,
                    "detected_source": result.detected_source_language
                    if hasattr(result, "detected_source_language")
                    else None,
                    "success": True,
                }
            except Exception as e:
                results[lang] = {"text": text, "error": str(e), "success": False}

        return results


async def batch_translate_captions(captions: list, target_language: str = "ES") -> list:
    translator = LiveCaptionTranslator(target_lang=target_language)

    tasks = []
    for caption in captions:
        if isinstance(caption, dict):
            text = caption.get("text", "")
            is_final = caption.get("is_final", True)
        else:
            text = str(caption)
            is_final = True

        tasks.append(translator.translate_caption(text, is_final))

    results = await asyncio.gather(*tasks, return_exceptions=True)

    translated_captions = []
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            original = captions[i] if i < len(captions) else {}
            translated_captions.append(
                {
                    "original": original.get("text", str(original))
                    if isinstance(original, dict)
                    else str(original),
                    "translated": original.get("text", str(original))
                    if isinstance(original, dict)
                    else str(original),
                    "error": str(result),
                    "success": False,
                }
            )
        else:
            translated_captions.append(result)

    return translated_captions


if __name__ == "__main__":

    async def mock_caption_stream():
        captions = [
            {"text": "Hello world", "is_final": True},
            {"text": "This is a test", "is_final": True},
            {"text": "Streaming translation", "is_final": False},
            {"text": "Final caption", "is_final": True},
        ]

        for caption in captions:
            yield caption
            await asyncio.sleep(0.5)

    async def main():
        translator = LiveCaptionTranslator(target_lang="ES")

        async for translated in translator.stream_translate_captions(
            mock_caption_stream()
        ):
            print(f"Original: {translated.get('text')}")
            print(f"Translated: {translated.get('translated_text')}")
            print(f"Metadata: {translated.get('translation_metadata')}")
            print("---")

    asyncio.run(main())
