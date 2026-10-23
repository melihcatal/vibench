import os
from google.cloud import translate_v2 as translate

def record_translate(text_to_translate: str, target_language: str = 'es') -> str:
    """
    Translates user-facing document fields using Google Cloud Translation.
    """
    # Google Cloud Translation uses GOOGLE_APPLICATION_CREDENTIALS for authentication.
    # Ensure this environment variable points to your service account key file.
    # For local testing, you might need to set:
    # os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "/path/to/your/keyfile.json"

    translate_client = translate.Client()

    if isinstance(text_to_translate, bytes):
        text_to_translate = text_to_translate.decode('utf-8')

    try:
        # Target language can be a language code like 'es' (Spanish) or 'fr' (French)
        response = translate_client.translate(
            text_to_translate, target_language=target_language
        )

        translated_text = response['translatedText']
        print(f"Original text: {text_to_translate}")
        print(f"Translated text ({target_language}): {translated_text}")
        return translated_text
    except Exception as e:
        print(f"Error translating text with Google Cloud Translation: {e}")
        raise

if __name__ == '__main__':
    # Example usage (requires GOOGLE_APPLICATION_CREDENTIALS env var)
    # os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "path/to/your/google_cloud_key.json" # Replace with actual path
    # english_text = "Hello, world! How are you today?"
    # spanish_translation = record_translate(english_text, 'es')
    # french_translation = record_translate(english_text, 'fr')
    # if spanish_translation:
    #     print(f"Spanish: {spanish_translation}")
    # if french_translation:
    #     print(f"French: {french_translation}")
    pass
