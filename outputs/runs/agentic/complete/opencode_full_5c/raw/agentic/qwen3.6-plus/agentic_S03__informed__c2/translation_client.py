import os
from typing import Optional

import deepl

from translation_models import (
    TranslationRequest,
    TranslationResponse,
    BatchTranslationRequest,
    BatchTranslationResponse,
    MarkupTranslationRequest,
    MarkupTranslationResponse,
    DictionaryTranslationRequest,
    DictionaryTranslationResponse,
    normalize_language_code,
    normalize_source_lang,
    build_translation_request_params,
)


class TranslationClient:
    def __init__(self, auth_key: Optional[str] = None):
        self.auth_key = auth_key or os.environ.get("DEEPL_AUTH_KEY", "")
        if not self.auth_key:
            raise ValueError("DEEPL_AUTH_KEY environment variable is required")
        self.client = deepl.Translator(self.auth_key)

    def translate(self, request: TranslationRequest) -> TranslationResponse:
        params = build_translation_request_params(request)
        result = self.client.translate_text(
            request.text,
            **params,
        )
        return TranslationResponse(
            translated_text=result.text,
            source_lang=normalize_source_lang(result.detected_source_lang),
            target_lang=normalize_language_code(result.target_lang),
            char_count=len(request.text),
            detected_source_lang=normalize_source_lang(result.detected_source_lang),
        )

    def batch_translate(
        self, request: BatchTranslationRequest
    ) -> BatchTranslationResponse:
        params = build_translation_request_params(request)
        results = self.client.translate_text(
            request.texts,
            **params,
        )
        translations = []
        total_chars = 0
        for i, result in enumerate(results):
            translations.append(
                TranslationResponse(
                    translated_text=result.text,
                    source_lang=normalize_source_lang(result.detected_source_lang),
                    target_lang=normalize_language_code(result.target_lang),
                    char_count=len(request.texts[i]),
                    detected_source_lang=normalize_source_lang(
                        result.detected_source_lang
                    ),
                )
            )
            total_chars += len(request.texts[i])
        return BatchTranslationResponse(
            translations=translations,
            total_char_count=total_chars,
        )

    def translate_markup(
        self, request: MarkupTranslationRequest
    ) -> MarkupTranslationResponse:
        params = build_translation_request_params(request)
        params["tag_handling"] = request.tag_handling
        if request.non_splitting_tags:
            params["non_splitting_tags"] = request.non_splitting_tags
        if request.ignore_tags:
            params["ignore_tags"] = request.ignore_tags
        result = self.client.translate_text(
            request.markup,
            **params,
        )
        return MarkupTranslationResponse(
            translated_markup=result.text,
            source_lang=normalize_source_lang(result.detected_source_lang),
            target_lang=normalize_language_code(result.target_lang),
            char_count=len(request.markup),
        )

    def translate_dictionary_values(
        self, request: DictionaryTranslationRequest
    ) -> DictionaryTranslationResponse:
        params = build_translation_request_params(request)
        texts = list(request.data.values())
        if not texts:
            return DictionaryTranslationResponse(
                translated_data={},
                source_lang=normalize_language_code(request.source_lang),
                target_lang=normalize_language_code(request.target_lang),
                total_char_count=0,
            )
        results = self.client.translate_text(texts, **params)
        translated_data = {}
        total_chars = 0
        for i, (key, _) in enumerate(request.data.items()):
            translated_data[key] = results[i].text
            total_chars += len(_)
        return DictionaryTranslationResponse(
            translated_data=translated_data,
            source_lang=normalize_source_lang(results[0].detected_source_lang),
            target_lang=normalize_language_code(results[0].target_lang),
            total_char_count=total_chars,
        )


def get_client(auth_key: Optional[str] = None) -> TranslationClient:
    return TranslationClient(auth_key=auth_key)
