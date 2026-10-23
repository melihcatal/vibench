import os
import deepl
from typing import List, Dict, Any
from speech_models import TranscriptionResult, TimestampedTranscript


def translate_transcript_segments(
    transcript: TranscriptionResult, target_language: str = "DE"
) -> Dict[str, Any]:
    """
    Translate completed transcript segments using DeepL API.

    Args:
        transcript: TranscriptionResult object
        target_language: Target language code (e.g., DE, FR, ES, JA, etc.)

    Returns:
        Dictionary with original and translated segments
    """
    # Get DeepL API key from environment
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set")

    # Initialize DeepL translator
    translator = deepl.Translator(auth_key)

    # Prepare segments for translation
    segments = []
    if hasattr(transcript, "segments") and transcript.segments:
        # Use timestamped segments if available
        for segment in transcript.segments:
            segments.append(
                {
                    "text": segment["text"],
                    "start_time": segment["start_time"],
                    "end_time": segment["end_time"],
                }
            )
    else:
        # Split transcript into sentences
        import re

        sentences = re.split(r"(?<=[.!?])\s+", transcript.transcript)
        segments = [
            {"text": sent, "start_time": None, "end_time": None}
            for sent in sentences
            if sent
        ]

    # Translate segments
    translated_segments = []
    for segment in segments:
        try:
            result = translator.translate_text(
                segment["text"], target_lang=target_language
            )

            translated_segments.append(
                {
                    "original_text": segment["text"],
                    "translated_text": result.text,
                    "start_time": segment["start_time"],
                    "end_time": segment["end_time"],
                    "detected_source_language": result.detected_source_lang,
                    "target_language": target_language,
                }
            )

        except deepl.DeepLException as e:
            print(f"Error translating segment: {e}")
            translated_segments.append(
                {
                    "original_text": segment["text"],
                    "translated_text": f"[TRANSLATION ERROR: {str(e)}]",
                    "start_time": segment["start_time"],
                    "end_time": segment["end_time"],
                    "detected_source_language": "UNKNOWN",
                    "target_language": target_language,
                }
            )

    # Get supported languages
    usage = translator.get_usage()

    return {
        "job_id": transcript.job_id,
        "original_language": transcript.language_code,
        "target_language": target_language,
        "segments": translated_segments,
        "total_segments": len(translated_segments),
        "character_count": sum(
            len(seg["original_text"]) for seg in translated_segments
        ),
        "deepl_usage": {
            "character_count": usage.character.count,
            "character_limit": usage.character.limit,
            "character_limit_reached": usage.any_limit_reached,
        },
    }


def translate_full_transcript(
    text: str, target_language: str = "DE", source_language: str = "EN"
) -> str:
    """
    Translate full transcript text using DeepL API.

    Args:
        text: Text to translate
        target_language: Target language code
        source_language: Source language code (auto-detected if None)

    Returns:
        Translated text
    """
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set")

    translator = deepl.Translator(auth_key)

    try:
        if source_language:
            result = translator.translate_text(
                text, source_lang=source_language, target_lang=target_language
            )
        else:
            result = translator.translate_text(text, target_lang=target_language)

        return result.text

    except deepl.DeepLException as e:
        print(f"Error translating text: {e}")
        raise


def get_supported_languages() -> List[Dict[str, str]]:
    """
    Get list of languages supported by DeepL.

    Returns:
        List of language dictionaries
    """
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set")

    translator = deepl.Translator(auth_key)

    source_languages = translator.get_source_languages()
    target_languages = translator.get_target_languages()

    return {
        "source_languages": [
            {"code": lang.code, "name": lang.name} for lang in source_languages
        ],
        "target_languages": [
            {"code": lang.code, "name": lang.name} for lang in target_languages
        ],
    }


if __name__ == "__main__":
    # Example usage
    import sys

    # Check for DeepL API key
    if not os.environ.get("DEEPL_AUTH_KEY"):
        print("Please set DEEPL_AUTH_KEY environment variable")
        sys.exit(1)

    if len(sys.argv) > 2:
        text = sys.argv[1]
        target_lang = sys.argv[2]
        translated = translate_full_transcript(text, target_lang)
        print(f"Translated text: {translated}")
    else:
        print("Usage: python translate_transcript.py <text> <target_language>")
        print("Example: python translate_transcript.py 'Hello world' DE")
