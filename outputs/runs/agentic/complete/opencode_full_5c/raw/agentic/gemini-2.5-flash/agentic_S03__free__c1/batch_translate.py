import os
from translation_client import TranslationClient
from translation_models import BatchTranslationRequest

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")


def batch_translate(request: BatchTranslationRequest) -> list[str]:
    if not PROJECT_ID:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")
    client = TranslationClient(project_id=PROJECT_ID)
    return client.batch_translate_texts(
        request.texts, request.target_language, request.source_language
    )
