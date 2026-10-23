import os
from google.cloud import translate_v3 as translate
from observability_models import TranslationRequest, TranslationResponse

def translate_log_message(
    request: TranslationRequest,
    project_id: str = None,
) -> TranslationResponse:
    """Translates support-visible log messages for another locale using Google Cloud Translation API."""

    if project_id is None:
        project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
        if not project_id:
            raise ValueError("project_id must be provided or GOOGLE_CLOUD_PROJECT env var set.")

    client = translate.TranslationServiceClient()

    parent = f"projects/{project_id}/locations/global"

    print(f"Translating log message to {request.target_language_code}...")
    try:
        response = client.translate_text(
            request=translate.TranslateTextRequest(
                parent=parent,
                contents=[request.text],
                target_language_code=request.target_language_code,
                source_language_code=request.source_language_code,
                mime_type="text/plain",  # Mime type of the text. Can be "text/plain" or "text/html".
            )
        )

        translated_text = response.translations[0].translated_text
        detected_language_code = response.translations[0].detected_language_code

        return TranslationResponse(
            translated_text=translated_text,
            detected_language_code=detected_language_code
        )

    except Exception as e:
        print(f"Error translating log message: {e}")
        return TranslationResponse(
            translated_text=f"Translation failed: {e}",
            detected_language_code="err"
        )

if __name__ == "__main__":
    # Example usage:
    # Set GOOGLE_CLOUD_PROJECT environment variable before running
    # export GOOGLE_CLOUD_PROJECT="your-gcp-project-id"
    # Enable Cloud Translation API for your project.

    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if project_id:
        print("\n--- Translating an English log message to Spanish ---")
        request_es = TranslationRequest(
            text="Database connection failed: Timeout occurred after 30 seconds.",
            target_language_code="es",
            source_language_code="en"
        )
        response_es = translate_log_message(request_es, project_id=project_id)
        print(f"Original: '{request_es.text}'")
        print(f"Translated (ES): '{response_es.translated_text}' (Detected: {response_es.detected_language_code})")

        print("\n--- Translating a German log message to English (auto-detect source) ---")
        request_en = TranslationRequest(
            text="Fehler beim Speichern der Benutzerdaten: Ungültige Eingabe.",
            target_language_code="en"
        )
        response_en = translate_log_message(request_en, project_id=project_id)
        print(f"Original: '{request_en.text}'")
        print(f"Translated (EN): '{response_en.translated_text}' (Detected: {response_en.detected_language_code})")

    else:
        print("Please set the GOOGLE_CLOUD_PROJECT environment variable.")
