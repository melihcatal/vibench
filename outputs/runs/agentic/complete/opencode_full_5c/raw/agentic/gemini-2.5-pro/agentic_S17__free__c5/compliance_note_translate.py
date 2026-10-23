from security_client import get_translation_client
from security_models import TranslationRequest


def translate_compliance_note(request: TranslationRequest) -> dict:
    """Translates encryption or compliance notes using Google Cloud Translate."""
    client = get_translation_client()

    result = client.translate(
        request.text,
        target_language=request.target_language,
        source_language=request.source_language,
    )
    return result
