import os
from translation_client import TranslationClient
from translation_models import MarkupTranslationRequest

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")


def translate_markup(request: MarkupTranslationRequest) -> str:
    if not PROJECT_ID:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")
    client = TranslationClient(project_id=PROJECT_ID)
    if request.format == "html":
        return client.translate_html(
            request.markup_text, request.target_language, request.source_language
        )
    else:
        # For plain text markup, we can use the regular text translation
        return client.translate_text(
            request.markup_text, request.target_language, request.source_language
        )
