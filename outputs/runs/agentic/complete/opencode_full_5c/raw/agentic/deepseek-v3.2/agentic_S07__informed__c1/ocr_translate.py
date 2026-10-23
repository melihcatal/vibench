import os
from typing import List, Optional
from document_client import DocumentClient
from document_models import TranslationResult


def translate_ocr_text(
    text: str,
    target_language: str,
    source_language: Optional[str] = None,
    region: Optional[str] = None,
) -> TranslationResult:
    client = DocumentClient(region_name=region)
    translate_client = client.get_translate_client()

    response = translate_client.translate_text(
        Text=text,
        SourceLanguageCode=source_language or "auto",
        TargetLanguageCode=target_language,
    )

    return TranslationResult(
        source_text=text,
        translated_text=response["TranslatedText"],
        source_language=response.get("SourceLanguageCode", source_language or "auto"),
        target_language=target_language,
    )


def translate_multiple_texts(
    texts: List[str],
    target_language: str,
    source_language: Optional[str] = None,
    region: Optional[str] = None,
) -> List[TranslationResult]:
    client = DocumentClient(region_name=region)
    translate_client = client.get_translate_client()

    results = []
    for text in texts:
        result = translate_ocr_text(text, target_language, source_language, region)
        results.append(result)

    return results


def translate_document_sections(
    sections: Dict[str, str], target_language: str, region: Optional[str] = None
) -> Dict[str, TranslationResult]:
    client = DocumentClient(region_name=region)
    translate_client = client.get_translate_client()

    translated_sections = {}
    for section_name, text in sections.items():
        if text:
            response = translate_client.translate_text(
                Text=text, SourceLanguageCode="auto", TargetLanguageCode=target_language
            )

            translated_sections[section_name] = TranslationResult(
                source_text=text,
                translated_text=response["TranslatedText"],
                source_language=response.get("SourceLanguageCode", "auto"),
                target_language=target_language,
            )

    return translated_sections


def detect_language(text: str, region: Optional[str] = None) -> str:
    client = DocumentClient(region_name=region)
    comprehend_client = client.get_comprehend_client()

    response = comprehend_client.detect_dominant_language(Text=text)

    if response["Languages"]:
        return response["Languages"][0]["LanguageCode"]

    return "en"


def translate_with_language_detection(
    text: str, target_language: str, region: Optional[str] = None
) -> TranslationResult:
    source_language = detect_language(text, region)

    return translate_ocr_text(
        text=text,
        target_language=target_language,
        source_language=source_language,
        region=region,
    )
