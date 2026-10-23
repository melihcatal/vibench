import os
from google.cloud import translate_v3 as translate

def translate_payload_text(text: str, target_language_code: str, project_id: str = None) -> str:
    """
    Translates the given text using Google Cloud Translation.
    """
    if project_id is None:
        project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
        if not project_id:
            raise ValueError("Google Cloud Project ID not provided and GOOGLE_CLOUD_PROJECT env var not set.")

    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language_code,
        }
    )

    translated_text = ""
    for translation in response.translations:
        translated_text += translation.translated_text
    
    return translated_text

if __name__ == "__main__":
    # Ensure GOOGLE_CLOUD_PROJECT is set in your environment
    if os.environ.get("GOOGLE_CLOUD_PROJECT"):
        original_text = "The quick brown fox jumps over the lazy dog."
        target_lang = "es" # Spanish

        print(f"Original text: {original_text}")
        translated_text = translate_payload_text(original_text, target_lang)
        print(f"Translated to {target_lang}: {translated_text}")

        original_text_zh = "你好，世界！"
        target_lang_en = "en" # English
        print(f"\nOriginal text: {original_text_zh}")
        translated_text_en = translate_payload_text(original_text_zh, target_lang_en)
        print(f"Translated to {target_lang_en}: {translated_text_en}")
    else:
        print("Please set the GOOGLE_CLOUD_PROJECT environment variable to run this example.")
