import os
from google.cloud import translate

def appeal_translate(text: str, target_language: str = 'en') -> dict:
    """
    Translates appeal text for review using Google Cloud Translation.
    The GOOGLE_APPLICATION_CREDENTIALS environment variable should be set for authentication.
    """
    client = translate.TranslationServiceClient()

    # The project ID is not directly passed to translate_text, it's inferred from credentials.
    # The parent format is `projects/{project_id}/locations/{location_id}`
    # For global location, use 'global'.
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID") # Assuming project ID is available, or use a default
    if not project_id:
        # Fallback if project_id is not explicitly set, hoping credentials will handle it.
        # In a real scenario, this should be explicitly configured.
        parent = f"projects/my-project-id/locations/global" # Placeholder, will rely on GOOGLE_APPLICATION_CREDENTIALS
    else:
        parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language,
        }
    )

    translations = []
    for translation in response.translations:
        translations.append({"translated_text": translation.translated_text, "detected_language_code": translation.detected_language_code})
    
    return {"original_text": text, "translations": translations}
