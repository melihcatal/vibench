"""
Translate completed transcript segments using AWS Translate.

Provider: AWS Translate (aws.translate)
SDK: boto3
Endpoint: translate.{region}.amazonaws.com
Model: aws.translate general translation service
"""

from typing import Optional

from speech_client import get_translate_client
from speech_models import Segment


def translate_transcript(
    transcript_text: str,
    source_language: str = "en",
    target_language: str = "es",
    terminology_name: Optional[str] = None,
) -> dict:
    """
    Translate a full transcript text using AWS Translate.

    Args:
        transcript_text: The source transcript to translate
        source_language: Source language code (ISO 639-1)
        target_language: Target language code (ISO 639-1)
        terminology_name: Optional custom terminology name for domain-specific terms

    Returns:
        dict with translated text and metadata
    """
    client = get_translate_client()

    kwargs = {
        "Text": transcript_text,
        "SourceLanguageCode": source_language,
        "TargetLanguageCode": target_language,
    }

    if terminology_name:
        kwargs["TerminologyNames"] = [terminology_name]

    response = client.translate_text(**kwargs)

    return {
        "translated_text": response.get("TranslatedText", ""),
        "source_language": response.get("SourceLanguageCode", source_language),
        "target_language": response.get("TargetLanguageCode", target_language),
        "detected_language": source_language,
    }


def translate_segments(
    segments: list[Segment],
    source_language: str = "en",
    target_language: str = "es",
    batch_size: int = 10,
) -> list[dict]:
    """
    Translate individual transcript segments using AWS Translate.

    Processes segments in batches for efficiency.

    Args:
        segments: List of Segment objects to translate
        source_language: Source language code
        target_language: Target language code
        batch_size: Number of segments per batch request

    Returns:
        list of dicts with original and translated segment data
    """
    client = get_translate_client()
    translated_results = []

    for i in range(0, len(segments), batch_size):
        batch = segments[i : i + batch_size]
        texts = [s.text for s in batch if s.text.strip()]

        if not texts:
            continue

        response = client.translate_text(
            Text=texts[0] if len(texts) == 1 else "\n".join(texts),
            SourceLanguageCode=source_language,
            TargetLanguageCode=target_language,
        )

        translated_text = response.get("TranslatedText", "")
        translated_parts = translated_text.split("\n")

        for idx, segment in enumerate(batch):
            translated = translated_parts[idx] if idx < len(translated_parts) else ""
            translated_results.append({
                "segment_id": segment.segment_id,
                "speaker": segment.speaker,
                "original_text": segment.text,
                "translated_text": translated,
                "start_time_ms": segment.start_time_ms,
                "end_time_ms": segment.end_time_ms,
                "source_language": source_language,
                "target_language": target_language,
            })

    return translated_results


def translate_with_custom_terminology(
    transcript_text: str,
    source_language: str,
    target_language: str,
    terminology_names: list[str],
) -> dict:
    """
    Translate transcript using AWS Translate with custom terminology.

    Args:
        transcript_text: Source text to translate
        source_language: Source language code
        target_language: Target language code
        terminology_names: List of custom terminology names to apply

    Returns:
        dict with translated text
    """
    client = get_translate_client()

    response = client.translate_text(
        Text=transcript_text,
        SourceLanguageCode=source_language,
        TargetLanguageCode=target_language,
        TerminologyNames=terminology_names,
    )

    return {
        "translated_text": response.get("TranslatedText", ""),
        "source_language": response.get("SourceLanguageCode"),
        "target_language": response.get("TargetLanguageCode"),
        "terminology_applied": terminology_names,
    }


def detect_and_translate(
    transcript_text: str,
    target_language: str,
) -> dict:
    """
    Auto-detect source language and translate using AWS Translate.

    AWS Translate automatically detects source language when set to 'auto'.

    Args:
        transcript_text: Text to detect and translate
        target_language: Target language code

    Returns:
        dict with detected language and translation
    """
    client = get_translate_client()

    response = client.translate_text(
        Text=transcript_text,
        SourceLanguageCode="auto",
        TargetLanguageCode=target_language,
    )

    return {
        "translated_text": response.get("TranslatedText", ""),
        "detected_source_language": response.get("SourceLanguageCode"),
        "target_language": response.get("TargetLanguageCode"),
    }
