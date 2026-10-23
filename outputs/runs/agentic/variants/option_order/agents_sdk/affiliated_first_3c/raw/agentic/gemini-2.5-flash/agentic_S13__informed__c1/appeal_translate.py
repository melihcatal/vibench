import os
from google.cloud import translate

def appeal_translate(text: str, target_language: str = "en", project_id: str = None):
    # For Google Cloud Translation, GOOGLE_APPLICATION_CREDENTIALS should be set up
    # or project_id explicitly provided if not using default credentials.
    
    client = translate.TranslationServiceClient()
    
    if project_id is None:
        # Attempt to get project_id from GOOGLE_CLOUD_PROJECT env var or default gcloud config
        # For this example, we'll assume it's either provided or set in the environment for simplicity.
        project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
        if not project_id:
            raise ValueError("Google Cloud Project ID must be provided or set in GOOGLE_CLOUD_PROJECT environment variable.")

    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language,
        }
    )

    translated_text = response.translations[0].translated_text if response.translations else ""
    return translated_text
