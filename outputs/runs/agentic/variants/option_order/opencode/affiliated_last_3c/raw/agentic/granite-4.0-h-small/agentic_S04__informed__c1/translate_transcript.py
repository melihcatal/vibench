import os
from speech_client import BatchSpeechClient
from speech_models import TranslationRequest, TranslationResponse
from google.cloud import translate_v2 as translate  # Google Cloud Translation provider


def translate_transcript(job_id: str, target_lang: str = "es") -> list[str]:
    """Translates completed transcript segments to the target language.

    Args:
        job_id: Identifier of the transcription job (used to retrieve transcript).
        target_lang: ISO 639-1 language code (default \"es\" for Spanish).

    Returns:
        List of translated paragraph / sentence strings.
    """
    client = BatchSpeechClient()
    # Retrieve the original transcript from the provider (placeholder)
    original_text = client.get_transcription_result(job_id=job_id, timeout=60)
    # Initialize Google Translation client
    translator = translate.Client()
    # Split transcript into manageable chunks (here we do simple line splits)
    chunks = [line for line in original_text.splitlines() if line.strip()]
    translations = []
    for chunk in chunks:
        request: TranslationRequest = {
            "text": chunk,
            "source_lang": "en",
            "target_lang": target_lang,
        }
        response = translator.translate(
            chunk,
            source_language=request["source_lang"],
            target_language=request["target_lang"],
        )
        translations.append(response["translatedText"])
    return translations
