import os
from google.cloud import translate
from security_models import TranslationRequest, TranslationResponse


def translate_compliance_note(request: TranslationRequest) -> TranslationResponse:
    """Translates encryption or compliance notes for reviewers using Google Cloud Translation.

    Args:
        request: A TranslationRequest object containing the text to translate, target language, and source language.

    Returns:
        A TranslationResponse object with the translated text.
    """
    # Create a client
    translate_client = translate.TranslationServiceClient()

    # The Google Cloud project ID can often be inferred from the environment
    # or explicitly set.
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        # Attempt to get project ID from default credentials if GOOGLE_CLOUD_PROJECT is not set
        try:
            import google.auth

            credentials, project_id = google.auth.default()
            if not project_id:
                raise ValueError(
                    "Google Cloud Project ID could not be determined. Set GOOGLE_CLOUD_PROJECT environment variable or ensure default credentials have a project set."
                )
        except Exception as e:
            raise ValueError(f"Could not determine Google Cloud Project ID: {e}")

    location = "global"  # Or specify a region like 'us-central1'
    parent = f"projects/{project_id}/locations/{location}"

    try:
        # Translate text
        response = translate_client.translate_text(
            request={
                "parent": parent,
                "contents": [request.text],
                "mime_type": "text/plain",  # Mime types: "text/plain" or "text/html"
                "source_language_code": request.source_language,
                "target_language_code": request.target_language,
            }
        )

        # Access translated text
        translated_text = response.translations[0].translated_text

        return TranslationResponse(translated_text=translated_text)
    except Exception as e:
        raise RuntimeError(
            f"Error translating compliance note with Google Cloud Translation: {e}"
        )
