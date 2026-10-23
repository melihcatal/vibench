from google.cloud import translate_v2 as translate
import os

def translate_text_google_cloud(text: str, target_language: str, project_id: str) -> str:
    """Translates text into the target language using Google Cloud Translation.
    Requires GOOGLE_APPLICATION_CREDENTIALS to be set up.
    """
    client = translate.Client(project=project_id)

    try:
        result = client.translate(text, target_language=target_language)
        translated_text = result['translatedText']
        print(f"Original Text: {text}")
        print(f"Translated Text ({target_language}): {translated_text}")
        return translated_text
    except Exception as e:
        print(f"Error translating text with Google Cloud Translation: {e}")
        raise

if __name__ == "__main__":
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
    text_to_translate = "Hello, how are you?"
    target_lang = "es"

    if not project_id:
        print("Please set GOOGLE_CLOUD_PROJECT_ID environment variable and ensure GOOGLE_APPLICATION_CREDENTIALS are set.")
    else:
        print("\n--- Translating sample text ---")
        translate_text_google_cloud(text_to_translate, target_lang, project_id)
        translate_text_google_cloud("How's life today?", "fr", project_id)
