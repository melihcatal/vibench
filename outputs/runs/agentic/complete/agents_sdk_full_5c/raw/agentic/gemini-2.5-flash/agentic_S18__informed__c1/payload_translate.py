import os
from google.cloud import translate_v3 as translate

def translate_text_payload(text: str, target_language_code: str, project_id: str) -> str:
    """Translates customer-facing message payload text using Google Cloud Translation."""
    client = translate.TranslationServiceClient()

    location = "global"  # Or a specific region, e.g., "us-central1"
    parent = f"projects/{project_id}/locations/{location}"

    # Wrap the text in a list for the request
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language_code,
        }
    )

    # The response contains a list of translations. We requested one text, so take the first.
    if response.translations:
        return response.translations[0].translated_text
    return f"Translation failed for: {text}"

if __name__ == '__main__':
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        print("Please set GOOGLE_CLOUD_PROJECT environment variable.")
    else:
        english_text = "Hello, how are you? Welcome to our service."
        target_lang = "es" # Spanish
        translated_text = translate_text_payload(english_text, target_lang, project_id)
        print(f"Original (en): {english_text}")
        print(f"Translated ({target_lang}): {translated_text}\n")

        french_text = "Merci de votre message."
        target_lang = "en" # English
        translated_text_back = translate_text_payload(french_text, target_lang, project_id)
        print(f"Original (fr): {french_text}")
        print(f"Translated ({target_lang}): {translated_text_back}")
