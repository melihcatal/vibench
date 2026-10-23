import os
import deepl


def translate_transcript(transcript_text, target_language="DE"):
    """Translate completed transcript segments using DeepL API."""
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable is required")

    translator = deepl.Translator(auth_key)

    try:
        result = translator.translate_text(transcript_text, target_lang=target_language)

        return {
            "original_text": transcript_text,
            "translated_text": result.text,
            "target_language": target_language,
            "detected_source_language": result.detected_source_language,
            "provider": "DeepL",
        }
    except deepl.DeepLException as e:
        return {"error": str(e), "provider": "DeepL"}


def translate_segments(segments, target_language="DE"):
    """Translate multiple transcript segments."""
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable is required")

    translator = deepl.Translator(auth_key)

    translated_segments = []

    for segment in segments:
        if isinstance(segment, dict):
            text = segment.get("text", "")
        else:
            text = str(segment)

        try:
            result = translator.translate_text(text, target_lang=target_language)

            translated_segments.append(
                {
                    "original": text,
                    "translated": result.text,
                    "detected_source_language": result.detected_source_language,
                }
            )
        except deepl.DeepLException as e:
            translated_segments.append({"original": text, "error": str(e)})

    return {
        "segments": translated_segments,
        "target_language": target_language,
        "provider": "DeepL",
    }
