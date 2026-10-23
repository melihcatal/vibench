import os
from typing import List, Optional
from google.cloud import translate_v2 as translate
from document_models import TextExtractionResponse


def translate_ocr_text(
    text: str, target_language: str, source_language: Optional[str] = None
) -> str:
    """
    Translate extracted OCR text using Google Cloud Translation.
    """
    credentials_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if not credentials_path or not os.path.exists(credentials_path):
        raise ValueError(
            "GOOGLE_APPLICATION_CREDENTIALS environment variable must point to valid credentials file"
        )

    translate_client = translate.Client()

    if source_language:
        result = translate_client.translate(
            text, target_language=target_language, source_language=source_language
        )
    else:
        result = translate_client.translate(text, target_language=target_language)

    return result["translatedText"]


def translate_extracted_text(
    extraction_response: TextExtractionResponse, target_language: str
) -> TextExtractionResponse:
    """
    Translate text from an OCR extraction response.
    """
    translated_text = translate_ocr_text(
        extraction_response.text, target_language, extraction_response.language
    )

    return TextExtractionResponse(
        text=translated_text,
        raw_response={
            "original": extraction_response.raw_response,
            "translation": translated_text,
            "target_language": target_language,
            "source_language": extraction_response.language,
        },
        provider="google_cloud_translation",
        confidence=extraction_response.confidence,
        language=target_language,
    )


def batch_translate_texts(
    texts: List[str], target_language: str, source_language: Optional[str] = None
) -> List[str]:
    """
    Translate multiple texts in batch using Google Cloud Translation.
    """
    credentials_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if not credentials_path or not os.path.exists(credentials_path):
        raise ValueError(
            "GOOGLE_APPLICATION_CREDENTIALS environment variable must point to valid credentials file"
        )

    translate_client = translate.Client()

    if source_language:
        results = translate_client.translate(
            texts, target_language=target_language, source_language=source_language
        )
    else:
        results = translate_client.translate(texts, target_language=target_language)

    return [result["translatedText"] for result in results]
