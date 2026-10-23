import os
from typing import List, Optional, Dict
from google.cloud import translate_v3 as google_translate
from translation_models import (
    TranslationRequest,
    BatchTranslationRequest,
    TranslationResponse,
    BatchTranslationResponse,
    MarkupTranslationRequest,
    MarkupTranslationResponse,
    DictionaryTranslationRequest,
    DictionaryTranslationResponse,
)


class GoogleTranslationClient:
    def __init__(self):
        self.client = google_translate.TranslationServiceClient()
        self.parent = f"projects/{os.getenv('GOOGLE_PROJECT_ID')}/locations/global"

    def translate_text(self, request: TranslationRequest) -> TranslationResponse:
        response = self.client.translate_text(
            parent=self.parent,
            contents=[request["text"]],
            mime_type="text/plain",
            source_language_code=request.get("source_lang"),
            target_language_code=request["target_lang"],
        )
        return TranslationResponse(
            translated_text=response.translations[0].translated_text,
            detected_source_lang=response.translations[0].detected_language_code,
        )

    def batch_translate(self, request: BatchTranslationRequest) -> BatchTranslationResponse:
        response = self.client.translate_text(
            parent=self.parent,
            contents=request["texts"],
            mime_type="text/plain",
            source_language_code=request.get("source_lang"),
            target_language_code=request["target_lang"],
        )
        return BatchTranslationResponse(
            translations=[
                TranslationResponse(
                    translated_text=translation.translated_text,
                    detected_source_lang=translation.detected_language_code,
                )
                for translation in response.translations
            ]
        )

    def _extract_text_from_markup(self, markup: str, protected_tags: Optional[List[str]] = None) -> List[str]:
        # Simplified extraction logic for demonstration
        import re
        protected_tags = protected_tags or []
        tag_pattern = re.compile("|.".join(protected_tags)) if protected_tags else None
        if tag_pattern:
            parts = tag_pattern.split(markup)
            texts = []
            for i, part in enumerate(parts):
                if i % 2 == 0:
                    texts.append(part)
            return texts
        return [markup]

    def _reconstruct_markup(self, markup: str, translated_texts: List[str], protected_tags: Optional[List[str]] = None) -> str:
        # Simplified reconstruction logic for demonstration
        import re
        protected_tags = protected_tags or []
        tag_pattern = re.compile("|.".join(protected_tags)) if protected_tags else None
        if tag_pattern:
            parts = tag_pattern.split(markup)
            text_index = 0
            for i in range(len(parts)):
                if i % 2 == 0 and text_index < len(translated_texts):
                    parts[i] = translated_texts[text_index]
                    text_index += 1
            return "".join(parts)
        return translated_texts[0]

    def translate_markup(self, request: MarkupTranslationRequest) -> MarkupTranslationResponse:
        texts = self._extract_text_from_markup(request.markup, request.protected_tags)
        batch_request = BatchTranslationRequest(
            texts=texts,
            source_lang=request.source_lang,
            target_lang=request.target_lang,
        )
        batch_response = self.batch_translate(batch_request)
        translated_markup = self._reconstruct_markup(
            request.markup,
            [t.translated_text for t in batch_response.translations],
            request.protected_tags,
        )
        return MarkupTranslationResponse(translated_markup=translated_markup)

    def translate_dictionary_values(self, request: DictionaryTranslationRequest) -> DictionaryTranslationResponse:
        batch_request = BatchTranslationRequest(
            texts=list(request.dictionary.values()),
            source_lang=request.source_lang,
            target_lang=request.target_lang,
        )
        batch_response = self.batch_translate(batch_request)
        translated_dictionary = {
            key: batch_response.translations[i].translated_text
            for i, key in enumerate(request.dictionary.keys())
        }
        return DictionaryTranslationResponse(translated_dictionary=translated_dictionary)