import os
from google.cloud import translate_v3 as translate

def translate_text(project_id: str, text: str, target_language: str, source_language: Optional[str] = None) -> str:
    """Translates text using Google Cloud Translation API."""
    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}"

    if source_language:
        response = client.translate_text(
            request={
                "parent": parent,
                "contents": [text],
                "target_language_code": target_language,
                "source_language_code": source_language,
            }
        )
    else:
        response = client.translate_text(
            request={
                "parent": parent,
                "contents": [text],
                "target_language_code": target_language,
            }
        )

    if response.translations:
        return response.translations[0].translated_text
    return ""

if __name__ == '__main__':
    # Example usage
    # project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    # if project_id:
    #     text_to_translate = "Hello, how are you?"
    #     target_lang = "es"
    #     translated = translate_text(project_id, text_to_translate, target_lang)
    #     print(f"Original: {text_to_translate}")
    #     print(f"Translated to {target_lang}: {translated}")
    #
    #     text_to_translate_fr = "Bonjour, comment ça va?"
    #     target_lang_en = "en"
    #     source_lang_fr = "fr"
    #     translated_en = translate_text(project_id, text_to_translate_fr, target_lang_en, source_language_fr)
    #     print(f"Original: {text_to_translate_fr}")
    #     print(f"Translated to {target_lang_en} (from {source_lang_fr}): {translated_en}")
    # else:
    #     print("Please set the GOOGLE_CLOUD_PROJECT environment variable.")
    pass
