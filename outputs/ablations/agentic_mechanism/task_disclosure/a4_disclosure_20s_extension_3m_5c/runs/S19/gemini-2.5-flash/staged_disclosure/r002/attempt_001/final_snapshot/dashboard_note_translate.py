
import os
from google.cloud import translate_v2 as translate

def translate_note(text: str, target_language: str, project_id: str) -> str:
    """Translates text into the target language using Google Cloud Translation API."""
    
    # Google Cloud Translation API client
    # The client will use the credentials configured in the environment (e.g., GOOGLE_APPLICATION_CREDENTIALS)
    client = translate.Client(project=project_id)

    # Translate the text
    # target_language can be a language code (e.g., "es" for Spanish, "fr" for French)
    result = client.translate(text, target_language=target_language)

    return result["translatedText"]


if __name__ == "__main__":
    # Example usage:
    # Set your Google Cloud Project ID and target language
    # You should have GOOGLE_APPLICATION_CREDENTIALS environment variable set
    # pointing to your service account key file.
    # For more info: https://cloud.google.com/docs/authentication/getting-started

    project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
    if not project_id:
        print("Error: GOOGLE_CLOUD_PROJECT_ID environment variable not set.")
        print("Please set it to your Google Cloud project ID.")
    else:
        text_to_translate = "This is a dashboard note about sales performance."
        target_lang = "es"  # Spanish

        print(f"Original text: {text_to_translate}")
        print(f"Target language: {target_lang}")

        try:
            translated_text = translate_note(text_to_translate, target_lang, project_id)
            print(f"Translated text: {translated_text}")
        except Exception as e:
            print(f"An error occurred: {e}")
            print("Please ensure your Google Cloud credentials are set up correctly and the Translation API is enabled for your project.")

