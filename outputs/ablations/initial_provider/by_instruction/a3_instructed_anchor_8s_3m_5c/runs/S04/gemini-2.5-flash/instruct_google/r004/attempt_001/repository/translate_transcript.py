from google.cloud import translate_v3 as translate
from speech_models import TranscriptionResult, TranscriptionAlternative
from typing import List

def translate_transcript(transcript_result: TranscriptionResult, target_language_code: str) -> TranscriptionResult:
    """Translates completed transcript segments using Google Cloud Translation API.

    Args:
        transcript_result: The TranscriptionResult object containing the original transcript.
        target_language_code: The target language code for translation (e.g., "es" for Spanish).

    Returns:
        A new TranscriptionResult object with translated transcript segments.
    """
    client = translate.TranslationServiceClient()
    project_id = client.common_project_path("your-gcp-project-id")  # Replace with your GCP project ID

    translated_alternatives: List[TranscriptionAlternative] = []

    for original_alternative in transcript_result.alternatives:
        if not original_alternative.transcript:
            continue

        response = client.translate_text(
            request={
                "parent": project_id,
                "contents": [original_alternative.transcript],
                "target_language_code": target_language_code,
                "source_language_code": transcript_result.language_code,
            }
        )

        translated_text = response.translations[0].translated_text if response.translations else ""
        translated_alternatives.append(TranscriptionAlternative(
            transcript=translated_text,
            confidence=original_alternative.confidence,
            words=original_alternative.words  # Keep original word info for now
        ))
    
    return TranscriptionResult(
        alternatives=translated_alternatives,
        result_end_time=transcript_result.result_end_time,
        language_code=target_language_code # Update to target language code
    )
