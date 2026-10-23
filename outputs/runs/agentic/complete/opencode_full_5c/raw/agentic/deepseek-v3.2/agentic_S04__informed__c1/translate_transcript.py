import boto3
from typing import List, Dict, Any, Optional


def translate_transcript_segments(
    segments: List[Dict[str, Any]],
    target_language_code: str = "es",
    source_language_code: str = "en",
) -> List[Dict[str, Any]]:
    """
    Translate completed transcript segments using Amazon Translate.

    Args:
        segments: List of transcript segments with 'text' field
        target_language_code: Target language code (default: es for Spanish)
        source_language_code: Source language code (default: en for English)

    Returns:
        List of segments with added 'translated_text' field
    """
    translate_client = boto3.client("translate")

    translated_segments = []

    for segment in segments:
        text = segment.get("text", "")
        if not text.strip():
            translated_segments.append({**segment, "translated_text": ""})
            continue

        try:
            response = translate_client.translate_text(
                Text=text,
                SourceLanguageCode=source_language_code,
                TargetLanguageCode=target_language_code,
            )

            translated_text = response["TranslatedText"]

            translated_segment = {
                **segment,
                "translated_text": translated_text,
                "source_language": source_language_code,
                "target_language": target_language_code,
                "translation_applied": True,
            }

            translated_segments.append(translated_segment)

        except Exception as e:
            translated_segment = {
                **segment,
                "translated_text": text,
                "source_language": source_language_code,
                "target_language": target_language_code,
                "translation_applied": False,
                "translation_error": str(e),
            }
            translated_segments.append(translated_segment)

    return translated_segments


def translate_transcript_text(
    text: str, target_language_code: str = "es", source_language_code: str = "en"
) -> str:
    """
    Translate transcript text using Amazon Translate.

    Args:
        text: Transcript text to translate
        target_language_code: Target language code
        source_language_code: Source language code

    Returns:
        Translated text
    """
    translate_client = boto3.client("translate")

    if not text.strip():
        return text

    response = translate_client.translate_text(
        Text=text,
        SourceLanguageCode=source_language_code,
        TargetLanguageCode=target_language_code,
    )

    return response["TranslatedText"]


def translate_with_timestamps(
    segments: List[Dict[str, Any]], target_language_code: str = "es"
) -> List[Dict[str, Any]]:
    """
    Translate segments while preserving timestamp information.

    Args:
        segments: Segments with 'text', 'start_time', 'end_time' fields
        target_language_code: Target language code

    Returns:
        Translated segments with timestamps preserved
    """
    translated = translate_transcript_segments(segments, target_language_code)

    for i, segment in enumerate(translated):
        if "start_time" in segments[i] and "end_time" in segments[i]:
            segment["start_time"] = segments[i]["start_time"]
            segment["end_time"] = segments[i]["end_time"]

        if "speaker" in segments[i]:
            segment["speaker"] = segments[i]["speaker"]

    return translated


def batch_translate_transcript(
    transcript_data: Dict[str, Any], target_language_code: str = "es"
) -> Dict[str, Any]:
    """
    Translate an entire transcript result.

    Args:
        transcript_data: Transcript data from poll_transcription_job
        target_language_code: Target language code

    Returns:
        Translated transcript data
    """
    translated_data = transcript_data.copy()

    if "transcript" in transcript_data:
        translated_text = translate_transcript_text(
            transcript_data["transcript"], target_language_code
        )
        translated_data["translated_transcript"] = translated_text

    if "items" in transcript_data:
        items = transcript_data["items"]
        text_items = [item for item in items if item["type"] == "pronunciation"]

        if text_items:
            text_to_translate = " ".join(
                [item["alternatives"][0]["content"] for item in text_items]
            )

            translated_text = translate_transcript_text(
                text_to_translate, target_language_code
            )

            translated_data["translated_items_text"] = translated_text

    translated_data["translation_target"] = target_language_code
    translated_data["translation_applied"] = True

    return translated_data
