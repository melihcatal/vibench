import os
from google.cloud import (
    translate_v3beta1 as translate,
)  # Google Cloud Translation API SDK
from identity_models import TranslationRequest, TranslationResponse

GOOGLE_PROJECT_ID = os.environ.get("GOOGLE_PROJECT_ID", "your-gcp-project-id")


def translate_consent_copy(request: TranslationRequest) -> TranslationResponse:
    client = translate.TranslationServiceClient()

    # The parent format is `projects/{project_number}/locations/{location_id}`
    # For global resources, use `global` for the location_id.
    parent = f"projects/{GOOGLE_PROJECT_ID}/locations/global"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [request.text],
            "target_language_code": request.target_language,
            "source_language_code": request.source_language,
            "mime_type": "text/plain",  # Mime types: "text/plain" or "text/html"
        }
    )

    translated_text = response.translations[0].translated_text
    source_language_code = (
        response.translations[0].detected_language_code
        if not request.source_language
        else request.source_language
    )

    # Google Cloud Translation SDK import: google.cloud.translate_v3beta1
    return TranslationResponse(
        translated_text=translated_text, source_language=source_language_code
    )


if __name__ == "__main__":
    # To run this example, ensure GOOGLE_PROJECT_ID is set in your environment
    # and you have authenticated your Google Cloud SDK (e.g., `gcloud auth application-default login`).
    # Also, ensure 'google-cloud-translate' is installed: pip install google-cloud-translate

    test_requests = [
        TranslationRequest(
            text="Do you consent to sharing your profile information?",
            target_language="es",
            source_language="en",
        ),
        TranslationRequest(
            text="Doy mi consentimiento para compartir mi información de perfil.",
            target_language="en",
        ),
    ]

    for i, req in enumerate(test_requests):
        print(f"\n--- Translation Request {i + 1} ---")
        print(f"Original Text: {req.text}")
        try:
            response = translate_consent_copy(req)
            print(f"Translated Text: {response.translated_text}")
            print(f"Detected Source Language: {response.source_language}")
        except Exception as e:
            print(f"Error translating consent copy: {e}")
            print(
                "Please ensure 'google-cloud-translate' is installed and you are authenticated to Google Cloud."
            )
