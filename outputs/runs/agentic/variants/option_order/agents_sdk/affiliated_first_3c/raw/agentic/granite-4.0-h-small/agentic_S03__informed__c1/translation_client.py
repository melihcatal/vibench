# [HELPER] translation_client.py

import os
from google.cloud import translate_v2 as translate
from typing import List

class TranslationClient:
    """Wrapper around Google Cloud Translation client library providing unified request/response handling.

    Provider: Google Cloud Translation (identified by the google.cloud.translate_v2 import).
    Credentials are loaded from GOOGLE_APPLICATION_CREDENTIALS environment variable.
    """
    def __init__(self):
        self.client = translate.Client()

    def translate(self, request: 'TranslationRequest') -> 'TranslationResponse':
        # Google expects source text as a single string or list of strings
        response = self.client.translate(request.source_text, source_language=request.source_lang,
                                         target_language=request.target_lang, format_="text")
        return TranslationResponse(**response)

    def translate_batch(self, requests: List['TranslationRequest']) -> List['TranslationResponse']:
        # Batch translate using list of strings
        texts = [r.source_text for r in requests]
        source_languages = [r.source_lang for r in requests]
        target_languages = [r.target_lang for r in requests]
        # Google's batch_translate_text is only available in v3 API; fallback to looping
        results = []
        for txt, src, tgt in zip(texts, source_languages, target_languages):
            res = self.client.translate(txt, source_language=src, target_language=tgt, format_="text")
            results.append(TranslationResponse(**res))
        return results

# Simple dataclasses for request/response contracts
from dataclasses import dataclass

dict = __import__('dataclasses')
@dataclass
class TranslationRequest:
    model_id: str  # ignored for now, kept for extensibility
    source_lang: str
    target_lang: str
    source_text: str

dict = __import__('dataclasses')
@dataclass
class TranslationResponse:
    translated_text: str
    detected_source_language: str = ""
