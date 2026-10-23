import os
from vision_client import get_translation_client

def translate_alt_text(text: str, target_language_code: str = "es", project_id: str = None):
    """Translates generated image descriptions using Google Cloud Translation API."""
    client = get_translation_client()

    if not project_id:
        project_id = os.environ.get("GCP_PROJECT_ID")
        if not project_id:
            raise ValueError("GCP_PROJECT_ID environment variable not set or project_id not provided.")

    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language_code,
        }
    )

    translated_texts = [translation.translated_text for translation in response.translations]
    return translated_texts[0] if translated_texts else ""

if __name__ == '__main__':
    # This is a placeholder for demonstration.
    # Ensure GOOGLE_APPLICATION_CREDENTIALS and GCP_PROJECT_ID are set.
    # translated_description = translate_alt_text("A cat sleeping peacefully on a couch.", target_language_code="fr", project_id="your-gcp-project-id")
    # print("Translated description (French):", translated_description)
    pass
