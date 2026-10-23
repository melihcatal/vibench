from __future__ import annotations

from typing import List

from translation_client import get_azure_translator_client
from translation_models import BatchTranslationRequest, BatchTranslationResult, normalize_text_list


def batch_translate(source_language: str, target_language: str, texts: List[str]) -> BatchTranslationResult:
    client = get_azure_translator_client()
    request = BatchTranslationRequest(source_language=source_language, target_language=target_language, texts=normalize_text_list(texts))
    response = client.translate(body=request.texts, from_parameter=request.source_language, to=[request.target_language])
    translated_texts = []
    for item in response:
        translated_texts.append(item.translations[0].text if item.translations else "")
    return BatchTranslationResult(translated_texts=translated_texts, raw=response)
