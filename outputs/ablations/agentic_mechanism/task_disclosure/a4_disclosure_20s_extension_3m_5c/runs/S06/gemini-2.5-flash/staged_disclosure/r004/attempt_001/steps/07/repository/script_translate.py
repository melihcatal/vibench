import os
from google.cloud import translate_v3 as translate

def translate_text(text: str, project_id: str, target_language: str = "en") -> str:
    client = translate.TranslationServiceClient()
    location = "global"
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",
            "source_language_code": "auto",
            "target_language_code": target_language,
        }
    )

    for translation in response.translations:
        return translation.translated_text
    return ""

if __name__ == "__main__":
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set.")

    # Example usage:
    # text_to_translate = "Hola, ¿cómo estás?"
    # translated_text = translate_text(text_to_translate, project_id, "es")
    # print(f"Original: {text_to_translate}")
    # print(f"Translated: {translated_text}")
