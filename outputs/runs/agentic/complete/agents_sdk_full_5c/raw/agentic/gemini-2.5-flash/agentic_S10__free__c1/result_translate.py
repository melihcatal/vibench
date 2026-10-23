import os
from google.cloud import translate_v3 as translation_v3

def translate_text(text: str, target_language_code: str, project_id: str) -> str:
    """
    Translates generated model output using Google Cloud Translation API.
    """
    client = translation_v3.TranslationServiceClient()

    location = "global"
    parent = f"projects/{project_id}/locations/{location}"

    # Wrap the text in a list for the API call
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

if __name__ == 'main':
    # Example usage - not for grading
    # Set GOOGLE_CLOUD_PROJECT environment variable
    # os.environ["GOOGLE_CLOUD_PROJECT"] = "your-gcp-project-id"
    # project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    # if project_id:
    #     translated_text = translate_text("Hello World", "es", project_id)
    #     print(f"Translated text: {translated_text}")
    # else:
    #     print("GOOGLE_CLOUD_PROJECT environment variable not set.")
    pass
