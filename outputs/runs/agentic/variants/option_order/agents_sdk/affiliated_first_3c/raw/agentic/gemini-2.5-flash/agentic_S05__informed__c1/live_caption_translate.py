import os
from google.cloud import translate_v3 as translate
from google.api_core.exceptions import GoogleAPIError

def translate_caption(text: str, target_language_code: str, project_id: str) -> str:
    """Translates a given text caption into the target language using Google Cloud Translation.

    Args:
        text (str): The caption text to translate.
        target_language_code (str): The BCP-47 language code of the target language (e.g., "es" for Spanish).
        project_id (str): Your Google Cloud Project ID.

    Returns:
        str: The translated text.

    Raises:
        GoogleAPIError: If the translation API call fails.
    """
    client = translate.TranslationServiceClient() # Uses GOOGLE_APPLICATION_CREDENTIALS by default
    location = "global"
    parent = f"projects/{project_id}/locations/{location}"

    # Wrap the text in a list for the request
    response = client.translate_text(
        parent=parent,
        contents=[text],
        target_language_code=target_language_code,
        # source_language_code="en", # Optional: specify source language if known
    )

    if response.translations:
        translated_text = response.translations[0].translated_text
        print(f"Original: '{text}' -> Translated ({target_language_code}): '{translated_text}'")
        return translated_text
    else:
        return f"[Translation failed for '{text}']"


if __name__ == "__main__":
    # To run this, ensure GOOGLE_APPLICATION_CREDENTIALS and GOOGLE_CLOUD_PROJECT are set.
    # export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service-account-key.json"
    # export GOOGLE_CLOUD_PROJECT="your-gcp-project-id"
    print("Live caption translation using Google Cloud Translation.")

    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        print("Error: GOOGLE_CLOUD_PROJECT environment variable not set.")
    else:
        try:
            caption_to_translate = "Hello, how are you doing today?"
            target_lang = "es"
            translated_caption = translate_caption(caption_to_translate, target_lang, project_id)
            print(f"Translated caption: {translated_caption}")

            caption_to_translate_2 = "This is a very important meeting."
            target_lang_2 = "fr"
            translated_caption_2 = translate_caption(caption_to_translate_2, target_lang_2, project_id)
            print(f"Translated caption: {translated_caption_2}")

        except GoogleAPIError as e:
            print(f"Google Cloud Translation API Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
    
    print("Ensure GOOGLE_APPLICATION_CREDENTIALS and GOOGLE_CLOUD_PROJECT are set for execution.")
