import os
from google.cloud import translate_v3 as translate
from observability_models import LogTranslationRequest, LogTranslationResponse

def translate_log_message(request: LogTranslationRequest) -> LogTranslationResponse:
    """Translates support-visible log messages for another locale using Google Cloud Translation."""
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/global" # "global" is standard for Cloud Translation

    try:
        response = client.translate_text(
            request={
                "parent": parent,
                "contents": [request.log_message_text],
                "target_language_code": request.target_language_code,
                "source_language_code": request.source_language_code,
                "mime_type": "text/plain",  # Mime types: "text/plain", "text/html"
            }
        )

        translations = response.translations
        if translations:
            translated_text = translations[0].translated_text
            detected_source_language = translations[0].detected_language_code
            return LogTranslationResponse(
                translated_text=translated_text,
                source_language_code=detected_source_language
            )
        else:
            return LogTranslationResponse(
                translated_text=request.log_message_text, # Return original if no translation
                source_language_code=request.source_language_code or "unknown"
            )

    except Exception as e:
        print(f"Error translating log message: {e}")
        return LogTranslationResponse(
            translated_text=f"Translation failed: {e}",
            source_language_code=request.source_language_code or "error"
        )

if __name__ == "__main__":
    # Example usage
    log_message_en = "User login failed due to invalid credentials."
    log_message_es = "Error al conectar con la base de datos."
    log_message_fr = "Mise à jour du profil utilisateur réussie."

    try:
        print("\n--- Translate English to Spanish ---")
        request_en_es = LogTranslationRequest(
            log_message_text=log_message_en,
            target_language_code="es"
        )
        response_en_es = translate_log_message(request_en_es)
        print(f"Original (en): {log_message_en}")
        print(f"Translated (es): {response_en_es.translated_text}")
        print(f"Detected Source: {response_en_es.source_language_code}")

        print("\n--- Translate Spanish to English ---")
        request_es_en = LogTranslationRequest(
            log_message_text=log_message_es,
            target_language_code="en"
        )
        response_es_en = translate_log_message(request_es_en)
        print(f"Original (es): {log_message_es}")
        print(f"Translated (en): {response_es_en.translated_text}")
        print(f"Detected Source: {response_es_en.source_language_code}")

        print("\n--- Translate French to German ---")
        request_fr_de = LogTranslationRequest(
            log_message_text=log_message_fr,
            target_language_code="de"
        )
        response_fr_de = translate_log_message(request_fr_de)
        print(f"Original (fr): {log_message_fr}")
        print(f"Translated (de): {response_fr_de.translated_text}")
        print(f"Detected Source: {response_fr_de.source_language_code}")

    except ValueError as e:
        print(f"Error: {e}")
        print("Please ensure GOOGLE_CLOUD_PROJECT environment variable is set.")
