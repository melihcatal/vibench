import os
from google.cloud import translate_v3

def translate_text(text: str, target_language_code: str, project_id: str = None) -> str:
    """
    Translates text using Google Cloud Translation API.
    Requires GOOGLE_APPLICATION_CREDENTIALS environment variable or a default project_id.
    """
    if not project_id:
        project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
        if not project_id:
            raise ValueError("Google Cloud project ID not provided and GOOGLE_CLOUD_PROJECT env var not set.")

    client = translate_v3.TranslationServiceClient()
    location = "global"
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language_code,
        }
    )

    if response.translations:
        return response.translations[0].translated_text
    return ""

if __name__ == '__main__':
    # Example usage (requires GOOGLE_APPLICATION_CREDENTIALS and GOOGLE_CLOUD_PROJECT env vars)
    # translated = translate_text("Hello World", "es", project_id="your-gcp-project-id")
    # print(f"Translated text: {translated}")
    pass
