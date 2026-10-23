import os
from google.cloud import translate

def translate_platform_output(text: str, target_language_code: str, project_id: str) -> str:
    """Translates platform model output for another locale using Google Cloud Translation."""
    client = translate.TranslationServiceClient()
    location = "global"  # Or specify a region like "us-central1" for a regional endpoint

    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language_code,
        }
    )

    translations = [t.translated_text for t in response.translations]
    return translations[0] if translations else ""

if __name__ == '__main__':
    # Example usage (replace with your actual project_id)
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if project_id:
        original_text = "Hello, how are you today?"
        target_lang = "es"
        translated_text = translate_platform_output(original_text, target_lang, project_id)
        print(f"Original: {original_text}")
        print(f"Translated ({target_lang}): {translated_text}")

        original_text_fr = "Je suis très bien, merci."
        target_lang_en = "en"
        translated_text_en = translate_platform_output(original_text_fr, target_lang_en, project_id)
        print(f"Original: {original_text_fr}")
        print(f"Translated ({target_lang_en}): {translated_text_en}")
    else:
        print("Please set the GOOGLE_CLOUD_PROJECT environment variable.")
