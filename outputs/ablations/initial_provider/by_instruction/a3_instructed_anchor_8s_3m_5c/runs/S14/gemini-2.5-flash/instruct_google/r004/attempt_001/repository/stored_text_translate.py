from google.cloud import translate_v3 as translate

from storage_client import get_translate_client
from storage_models import StoredTextTranslateRequest, StoredTextTranslateResponse

def translate_stored_text(
    request: StoredTextTranslateRequest
) -> StoredTextTranslateResponse:
    """Translates text using Google Cloud Translation API."""
    client = get_translate_client()

    parent = f"projects/{request.project_id}/locations/{request.location}"

    response = client.translate_text(
        parent=parent,
        contents=[request.text],
        target_language_code=request.target_language_code,
        source_language_code=request.source_language_code,
        mime_type="text/plain",  # Mime types: "text/plain", "text/html"
    )

    # The translated text is in the first translation's `translated_text` field.
    translation = response.translations[0]

    return StoredTextTranslateResponse(
        translated_text=translation.translated_text,
        source_language_code=translation.detected_language_code,
    )
