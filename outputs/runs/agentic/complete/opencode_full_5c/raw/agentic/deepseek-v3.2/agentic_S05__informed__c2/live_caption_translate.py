import deepl
import os
from typing import List, Dict, Any, Optional
import asyncio
import queue
import threading


class LiveCaptionTranslator:
    def __init__(self, target_language: str = "DE"):
        self.auth_key = os.getenv("DEEPL_AUTH_KEY")
        if not self.auth_key:
            raise ValueError("DEEPL_AUTH_KEY environment variable must be set")

        self.translator = deepl.Translator(self.auth_key)
        self.target_language = target_language
        self.translation_queue = queue.Queue()
        self.result_queue = queue.Queue()
        self.is_translating = False

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
            "NB": "Norwegian Bokmål",
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

    def validate_target_language(self) -> bool:
        return self.target_language in self.supported_languages

    def translate_text(self, text: str, source_lang: Optional[str] = None) -> str:
        if not text or not text.strip():
            return ""

        try:
            result = self.translator.translate_text(
                text, source_lang=source_lang, target_lang=self.target_language
            )
            return result.text
        except Exception as e:
            print(f"Translation error: {e}")
            return text

    def translate_caption(self, caption: Dict[str, Any]) -> Dict[str, Any]:
        original_text = caption.get("text", "")
        is_final = caption.get("is_final", False)

        translated_text = self.translate_text(original_text)

        return {
            "original_text": original_text,
            "translated_text": translated_text,
            "target_language": self.target_language,
            "is_final": is_final,
            "timestamp": caption.get("timestamp"),
            "speaker_id": caption.get("speaker_id"),
        }

    def start_translation_stream(self):
        self.is_translating = True

        def translation_worker():
            while self.is_translating:
                try:
                    caption = self.translation_queue.get(timeout=0.1)
                    translated = self.translate_caption(caption)
                    self.result_queue.put(translated)
                except queue.Empty:
                    continue
                except Exception as e:
                    self.result_queue.put(
                        {"error": str(e), "original_caption": caption}
                    )

        self.worker_thread = threading.Thread(target=translation_worker)
        self.worker_thread.daemon = True
        self.worker_thread.start()

    def stop_translation_stream(self):
        self.is_translating = False
        if self.worker_thread:
            self.worker_thread.join(timeout=1)

    def add_caption_for_translation(self, caption: Dict[str, Any]):
        self.translation_queue.put(caption)

    def get_translated_captions(self):
        while True:
            try:
                yield self.result_queue.get(timeout=0.1)
            except queue.Empty:
                if not self.is_translating:
                    break
                continue

    async def stream_translate_captions(self, caption_stream):
        self.start_translation_stream()
        try:
            async for caption in caption_stream:
                self.add_caption_for_translation(caption)
                for translated in self.get_translated_captions():
                    yield translated
        finally:
            self.stop_translation_stream()

    def get_usage_info(self) -> Dict[str, Any]:
        try:
            usage = self.translator.get_usage()
            return {
                "character_count": usage.character.count,
                "character_limit": usage.character.limit,
                "document_count": usage.document.count
                if hasattr(usage, "document")
                else None,
                "document_limit": usage.document.limit
                if hasattr(usage, "document")
                else None,
                "team_document_count": usage.team_document.count
                if hasattr(usage, "team_document")
                else None,
                "team_document_limit": usage.team_document.limit
                if hasattr(usage, "team_document")
                else None,
            }
        except Exception as e:
            return {"error": str(e)}

    def get_supported_languages(self) -> Dict[str, str]:
        return self.supported_languages.copy()

    def set_target_language(self, language_code: str):
        if language_code not in self.supported_languages:
            raise ValueError(f"Unsupported language code: {language_code}")
        self.target_language = language_code
