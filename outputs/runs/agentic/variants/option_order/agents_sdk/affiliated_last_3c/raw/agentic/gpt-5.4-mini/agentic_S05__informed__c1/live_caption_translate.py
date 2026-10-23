from __future__ import annotations

import os

import boto3

from speech_models import TranslationResult


class LiveCaptionTranslator:
    def __init__(self, target_language: str = "es"):
        self.target_language = target_language
        self.client = boto3.client("translate")

    def translate(self, text: str, source_language: str = "en") -> TranslationResult:
        response = self.client.translate_text(
            Text=text,
            SourceLanguageCode=source_language,
            TargetLanguageCode=self.target_language,
        )
        return TranslationResult(
            source_text=text,
            translated_text=response["TranslatedText"],
            source_language=source_language,
            target_language=self.target_language,
            raw=response,
        )
