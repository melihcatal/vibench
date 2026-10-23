"""Translate platform model output for another locale using Amazon Translate.

Uses the boto3 Amazon Translate TranslateText API to convert generated
text into a target language, supporting over 70 language pairs.
Auth: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
Provider: Amazon Translate
"""

from typing import Optional

from model_client import get_translate_client
from model_models import TranslationResult


def localize_platform_output(
    text: str,
    target_language: str = "es",
    source_language: str = "en",
    aws_access_key_id: Optional[str] = None,
    aws_secret_access_key: Optional[str] = None,
) -> TranslationResult:
    """Translate platform model output using Amazon Translate.

    Calls the TranslateText API with the specified source and target
    language codes (e.g., 'en' to 'es' for English to Spanish).
    Returns a TranslationResult with the translated text and metadata.
    """
    if not text or not text.strip():
        return TranslationResult(
            translated_text="",
            source_language=source_language,
            target_language=target_language,
            raw_response={"message": "Empty input text"},
        )

    client = get_translate_client(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
    )

    params = {
        "Text": text,
        "TargetLanguageCode": target_language,
    }
    if source_language:
        params["SourceLanguageCode"] = source_language

    response = client.translate_text(**params)

    translated = response.get("TranslatedText", "")
    detected_source = response.get("SourceLanguageCode", source_language)

    return TranslationResult(
        translated_text=translated,
        source_language=detected_source,
        target_language=target_language,
        raw_response=response,
    )


def batch_localize_outputs(
    texts: list,
    target_language: str = "fr",
    source_language: str = "en",
    aws_access_key_id: Optional[str] = None,
    aws_secret_access_key: Optional[str] = None,
) -> list:
    """Translate multiple platform outputs in sequence."""
    results = []
    for text in texts:
        if text and text.strip():
            result = localize_platform_output(
                text=text,
                target_language=target_language,
                source_language=source_language,
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key,
            )
            results.append(result)
    return results


if __name__ == "__main__":
    sample = "The cloud platform provides scalable compute resources."
    result = localize_platform_output(sample, target_language="es", source_language="en")
    print(f"Source: {result.source_language}")
    print(f"Target: {result.target_language}")
    print(f"Translated: {result.translated_text}")
