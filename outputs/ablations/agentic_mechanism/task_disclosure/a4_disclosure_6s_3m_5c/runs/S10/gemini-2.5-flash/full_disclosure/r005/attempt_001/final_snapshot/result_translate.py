from google.cloud import translate_v3 as translate

def translate_text(text: str, target_language: str) -> str:
    """
    Translates the given text to the target language using Google Cloud Translation API.
    """
    client = translate.TranslationServiceClient()
    project_id = "YOUR_PROJECT_ID"  # Replace with your Google Cloud Project ID
    location = "global"

    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language,
        }
    )

    for translation in response.translations:
        return translation.translated_text
    return ""
