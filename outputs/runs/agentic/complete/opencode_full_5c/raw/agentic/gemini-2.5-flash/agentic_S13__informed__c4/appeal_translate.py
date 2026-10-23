import os
from google.cloud import translate


def translate_appeal_text(text: str, target_language: str = "en") -> str:
    # GOOGLE_APPLICATION_CREDENTIALS should be set in the environment
    # or the client will try to find default credentials.
    # For this example, we assume it's set up or will use default.

    # The GOOGLE_APPLICATION_CREDENTIALS environment variable is the provider-identifying signal.
    # No direct API key for Cloud Translation, it uses service account credentials.
    # If running locally, you might need to authenticate: gcloud auth application-default login

    client = translate.TranslationServiceClient()

    # A project ID is usually required for Cloud Translation. Assuming it's in the environment
    # or implicitly picked up by the credentials. For explicit project, it would be client.location_path(project_id, "global")
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        print(
            "Warning: GOOGLE_CLOUD_PROJECT environment variable not set. Translation might fail if implicit project ID isn't found."
        )
        # Fallback to a placeholder location path if project_id is not set, though this might not work without proper project context.
        location = "global"
    else:
        location = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        request={
            "parent": location,
            "contents": [text],
            "mime_type": "text/plain",
            "target_language_code": target_language,
        }
    )

    if response.translations:
        return response.translations[0].translated_text
    return text  # Return original text if translation fails
