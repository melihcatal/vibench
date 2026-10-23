import os
from google.cloud import translate_v3 as translate

def translate_text(text: str, target_language: str, project_id: str) -> str:
    """Translates a given text string into the target language using Google Cloud Translation API.

    Args:
        text: The text string to translate.
        target_language: The language code to translate the text into (e.g., "es" for Spanish).
        project_id: Your Google Cloud project ID.

    Returns:
        The translated text string.
    """
    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language,
        }
    )

    translated_text = response.translations[0].translated_text
    return translated_text

if __name__ == "__main__":
    # IMPORTANT: Replace with your actual Google Cloud Project ID
    # Ensure you have authenticated to Google Cloud and set up the GOOGLE_APPLICATION_CREDENTIALS
    # environment variable or configured your default credentials.
    # For more information, see:
    # https://cloud.google.com/docs/authentication/getting-started
    
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID", "your-google-cloud-project-id") 

    if project_id == "your-google-cloud-project-id":
        print("Please set the GOOGLE_CLOUD_PROJECT_ID environment variable or replace 'your-google-cloud-project-id' with your actual project ID.")
    else:
        text_to_translate = "Hello, world!"
        target_lang = "es"  # Translate to Spanish

        print(f"Translating: '{text_to_translate}' to '{target_lang}'")
        translated_result = translate_text(text_to_translate, target_lang, project_id)
        print(f"Translated text: {translated_result}")

        text_to_translate_french = "Bonjour le monde!"
        target_lang_english = "en" # Translate to English

        print(f"Translating: '{text_to_translate_french}' to '{target_lang_english}'")
        translated_result_english = translate_text(text_to_translate_french, target_lang_english, project_id)
        print(f"Translated text: {translated_result_english}")
