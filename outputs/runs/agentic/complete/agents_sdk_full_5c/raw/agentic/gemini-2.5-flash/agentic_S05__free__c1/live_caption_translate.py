from google.cloud import translate_v3 as translate

def translate_caption(text: str, target_language_code: str, project_id: str) -> str:
    """Translates a given text into the target language using Google Cloud Translation."""
    client = translate.TranslationServiceClient()

    location = "global"

    parent = f"projects/{project_id}/locations/{location}"

    # Translate text from English to the target language
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",  # Mime types: "text/plain", "text/html"
            "target_language_code": target_language_code,
        }
    )

    if response.translations:
        return response.translations[0].translated_text
    return ""

if __name__ == '__main__':
    # Replace with your Google Cloud Project ID
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set up.
    YOUR_PROJECT_ID = "your-gcp-project-id" # <<< IMPORTANT: Update with your project ID

    if YOUR_PROJECT_ID == "your-gcp-project-id":
        print("Please update YOUR_PROJECT_ID in live_caption_translate.py to your Google Cloud Project ID.")
    else:
        caption_to_translate = "Hello, how are you doing today?"
        translated_text = translate_caption(caption_to_translate, "es", YOUR_PROJECT_ID)
        print(f"Original: {caption_to_translate}")
        print(f"Translated (Spanish): {translated_text}")

        caption_to_translate_fr = "Ceci est un exemple de traduction."
        translated_text_en = translate_caption(caption_to_translate_fr, "en", YOUR_PROJECT_ID)
        print(f"Original (French): {caption_to_translate_fr}")
        print(f"Translated (English): {translated_text_en}")
