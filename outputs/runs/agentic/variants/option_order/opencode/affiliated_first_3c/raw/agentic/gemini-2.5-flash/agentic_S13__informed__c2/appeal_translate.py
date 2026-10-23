import os
from google.cloud import translate_v3 as translate


def translate_appeal_text(
    text: str, target_language: str = "en", project_id: str = None
):
    """
    Translates appeal text using Google Cloud Translation.
    Requires GOOGLE_APPLICATION_CREDENTIALS to be set up (e.g., via service account key file).
    Project ID can be provided or inferred from credentials.
    """
    client = translate.TranslationServiceClient()

    if not project_id:
        # Attempt to infer project_id if not provided
        # This often works if GOOGLE_APPLICATION_CREDENTIALS is set to a service account file
        try:
            import google.auth

            credentials, project_id = google.auth.default()
        except Exception:
            raise ValueError(
                "Google Cloud project_id must be provided or GOOGLE_APPLICATION_CREDENTIALS must be set for auto-detection."
            )

    parent = f"projects/{project_id}"

    try:
        response = client.translate_text(
            request={
                "parent": parent,
                "contents": [text],
                "target_language_code": target_language,
            }
        )
        translated_text = response.translations[0].translated_text
        return {
            "original_text": text,
            "translated_text": translated_text,
            "target_language": target_language,
        }
    except Exception as e:
        return {"error": str(e)}
