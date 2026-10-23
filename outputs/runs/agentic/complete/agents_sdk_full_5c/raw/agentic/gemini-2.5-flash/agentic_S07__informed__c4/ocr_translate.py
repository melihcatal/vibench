import os
from google.cloud import translate_v3 as translate

def translate_text_with_google_cloud(text: str, target_language: str, project_id: str, source_language: Optional[str] = None) -> str:
    """
    Translates text using Google Cloud Translation.
    """
    client = translate.TranslationServiceClient()

    parent = f"projects/{project_id}/locations/global"

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

    return response.translations[0].translated_text

if __name__ == '__main__':
    # Placeholder for actual usage, demonstrating the provider integration
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    text_to_translate = "Hello, world!"
    target_lang = "es"
    source_lang = "en"

    if project_id:
        print(f"Translating '{text_to_translate}' to '{target_lang}' using Google Cloud Translation...")
        # translated_text = translate_text_with_google_cloud(text_to_translate, target_lang, project_id, source_lang)
        # print("Translated Text:", translated_text)
    else:
        print("Please set GOOGLE_CLOUD_PROJECT environment variable.")
