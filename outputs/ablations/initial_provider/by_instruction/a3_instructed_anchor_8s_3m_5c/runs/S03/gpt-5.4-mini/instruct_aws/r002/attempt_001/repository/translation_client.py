import os
from typing import Any, Dict, List, Optional

import boto3

from translation_models import TranslationRequest, TranslationResult, normalize_mapping_values, normalize_text, normalize_text_list


class TranslationClient:
    def __init__(self, region_name: Optional[str] = None):
        self.region_name = region_name or os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1"
        self.client = boto3.client("translate", region_name=self.region_name)

    def translate_text(self, text: str, source_language: Optional[str], target_language: str) -> TranslationResult:
        request = TranslationRequest(text=normalize_text(text), source_language=source_language, target_language=target_language)
        kwargs: Dict[str, Any] = {"Text": request.text, "TargetLanguageCode": request.target_language}
        if request.source_language:
            kwargs["SourceLanguageCode"] = request.source_language
        response = self.client.translate_text(**kwargs)
        return TranslationResult(
            translated_text=response["TranslatedText"],
            source_language=response.get("SourceLanguageCode", request.source_language),
            target_language=response.get("TargetLanguageCode", request.target_language),
            provider="aws.translate",
        )

    def batch_translate_text(self, texts: List[str], source_language: Optional[str], target_language: str) -> List[TranslationResult]:
        return [self.translate_text(text, source_language, target_language) for text in normalize_text_list(texts)]

    def translate_markup(self, markup: str, source_language: Optional[str], target_language: str) -> TranslationResult:
        return self.translate_text(markup, source_language, target_language)

    def translate_dictionary_values(self, values: Dict[str, Any], source_language: Optional[str], target_language: str) -> Dict[str, TranslationResult]:
        normalized = normalize_mapping_values(values)
        return {key: self.translate_text(value, source_language, target_language) for key, value in normalized.items()}
