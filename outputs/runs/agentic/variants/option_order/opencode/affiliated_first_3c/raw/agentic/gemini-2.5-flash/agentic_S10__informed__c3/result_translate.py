import os
from google.cloud import translate
from model_models import TranslationRequest

# Google Cloud Translation: service=Cloud Translation; sdk=google-cloud-translate; interface=sdk; auth=GOOGLE_APPLICATION_CREDENTIALS


def translate_text(request: TranslationRequest) -> dict:
    # GOOGLE_APPLICATION_CREDENTIALS should be set in the environment
    # For local testing, ensure your gcloud is authenticated or GOOGLE_APPLICATION_CREDENTIALS points to a service account key file.
    # print("GOOGLE_APPLICATION_CREDENTIALS status:", "Set" if os.environ.get("GOOGLE_APPLICATION_CREDENTIALS") else "Not set")

    client = translate.TranslationServiceClient()

    project_id = os.environ.get(
        "GOOGLE_CLOUD_PROJECT_ID"
    )  # Optional, can be auto-detected if credentials are set up correctly
    if not project_id:
        # Fallback for local dev where project_id might not be explicitly set
        # In a deployed GCP environment, this is usually auto-detected
        try:
            import google.auth

            _, project_id = google.auth.default()
        except Exception:
            pass  # Will proceed with client.translate_text without explicit project if project_id is None

    parent = (
        f"projects/{project_id}" if project_id else None
    )  # The location path for the API call (e.g., "projects/project-id")
    # The translate_text method can infer the project from credentials or if running in GCP.

    response = client.translate_text(
        parent=parent,
        contents=[request.text],
        target_language_code=request.target_language,
        source_language_code=request.source_language
        if request.source_language
        else None,
        mime_type="text/plain",  # Can be "text/plain" or "text/html"
    )

    translated_texts = [
        translation.translated_text for translation in response.translations
    ]
    return {"translated_text": translated_texts[0] if translated_texts else ""}
