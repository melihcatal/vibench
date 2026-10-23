import json
from speech_models import TranscriptionResult, normalize_transcript
from translation_client import BatchTranslator


def translate_transcript(
    transcript: TranscriptionResult, target_lang: str = "es"
) -> List[str]:
    """Translate each segment of a completed transcript to a target language.

    Args:
        transcript (TranscriptionResult): Normalized transcript object.
        target_lang (str): ISO language code (e.g., "es", "fr").

    Returns:
        List[str]: List of translated segment texts.
    """
    translator = BatchTranslator()
    # Translate segment by segment to preserve timestamps later
    translated_segments = []
    for seg in transcript["segments"]:
        payload = {
            "text": seg["text"],
            "source_lang": transcript.get("language", "en"),
            "target_lang": target_lang,
        }
        response = translator.translate(payload)
        translated_segments.append(response["text"])
    return translated_segments


# Example (uncomment to test)
# if __name__ == "__main__":
#     # Assume we have a job_id from earlier steps
#     job = {"job_id": "job_123", "language": "en"}
#     result = poll_transcription(job["job_id"])
#     norm = normalize_transcript(result)
#     translations = translate_transcript(norm, target_lang="fr")
#     print(json.dumps(translations, indent=2))
