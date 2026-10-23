import os
from translation_client import TranslationClient
from translation_models import TranslationRequest

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")


def translate_text(request: TranslationRequest) -> str:
    if not PROJECT_ID:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")
    client = TranslationClient(project_id=PROJECT_ID)
    return client.translate_text(
        request.text, request.target_language, request.source_language
    )
