from translation_client import TranslationClient
from translation_models import BatchTranslationRequest
import os


def batch_translate(
    texts: list[str], target_language: str, source_language: str = None
) -> list[str]:
    """
    Translates a list of strings while preserving order using Google Cloud Translation API.
    """
    client = TranslationClient(os.getenv("GOOGLE_CLOUD_PROJECT_ID"))
    request = BatchTranslationRequest(
        texts=texts, target_language=target_language, source_language=source_language
    )

    results = []
    for text in request.texts:
        translated = client.translate_text(
            text, request.target_language, request.source_language
        )
        results.append(translated)

    return results
