import os
from google.cloud import translate_v3 as translate
from google.api_core.exceptions import GoogleAPIError
from security_client import get_translate_client
from security_models import TranslationRequest, TranslationResponse

def translate_compliance_note(request: TranslationRequest) -> TranslationResponse:
    """Translates encryption or compliance notes using Google Cloud Translation."""
    client = get_translate_client()

    # A translation client is created with a default project, but for clarity,
    # we can explicitly specify the project if needed.
    project_id = request.project_id or os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable or project_id in request not set for Google Cloud Translation.")

    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [request.text],
            "target_language_code": request.target_language_code,
            "source_language_code": request.source_language_code,
        }
    )

    translated_text = ""
    detected_source_language = None

    if response.translations:
        translated_text = response.translations[0].translated_text
        detected_source_language = response.translations[0].detected_language_code
    
    return TranslationResponse(
        translated_text=translated_text,
        detected_source_language=detected_source_language
    )

if __name__ == '__main__':
    # Example Usage
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set.
    # And GOOGLE_CLOUD_PROJECT environment variable is set.

    sample_compliance_note_en = "This encryption key must be rotated every 90 days as per regulatory compliance."
    sample_compliance_note_es = "Esta clave de cifrado debe rotarse cada 90 días según el cumplimiento normativo."

    try:
        print("Translating English compliance note to Spanish...")
        request_en_es = TranslationRequest(
            text=sample_compliance_note_en,
            target_language_code="es",
            source_language_code="en"
        )
        response_en_es = translate_compliance_note(request_en_es)
        print(f"Original (EN): {sample_compliance_note_en}")
        print(f"Translated (ES): {response_en_es.translated_text}")
        print(f"Detected source language: {response_en_es.detected_source_language}")

        print("\nTranslating Spanish compliance note to French (auto-detect source)...")
        request_es_fr = TranslationRequest(
            text=sample_compliance_note_es,
            target_language_code="fr"
        )
        response_es_fr = translate_compliance_note(request_es_fr)
        print(f"Original (ES): {sample_compliance_note_es}")
        print(f"Translated (FR): {response_es_fr.translated_text}")
        print(f"Detected source language: {response_es_fr.detected_source_language}")

    except ValueError as e:
        print(f"Error: {e}")
    except GoogleAPIError as e:
        print(f"Google Cloud Translation API error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
