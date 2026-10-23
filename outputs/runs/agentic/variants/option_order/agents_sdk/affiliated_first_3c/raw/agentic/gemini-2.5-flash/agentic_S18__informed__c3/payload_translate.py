from google.cloud import translate_v2 as translate
import os

def translate_payload_text(text: str, target_language_code: str, project_id: str) -> str:
    """Translates customer-facing message payload text using Google Cloud Translation.
    Requires GOOGLE_APPLICATION_CREDENTIALS to be set up.
    """
    if not project_id:
        raise ValueError("Google Cloud PROJECT_ID must be provided.")

    translate_client = translate.Client(project=project_id)

    # Target language can be an ISO 639-1 code.
    # See https://cloud.google.com/translate/docs/supported-languages
    result = translate_client.translate(
        text,
        target_language=target_language_code
    )

    print(f"Text: {result['input']}")
    print(f"Translation: {result['translatedText']}")
    print(f"Detected source language: {result['detectedSourceLanguage']}")

    return result['translatedText']

if __name__ == '__main__':
    # Example usage
    PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
    
    if not PROJECT_ID:
        print("Please set the GOOGLE_CLOUD_PROJECT_ID environment variable.")
    else:
        text_to_translate = "Hello, how are you? This is an important message."
        target_lang = "es" # Spanish
        
        try:
            translated_text = translate_payload_text(text_to_translate, target_lang, PROJECT_ID)
            print(f"\nOriginal: {text_to_translate}")
            print(f"Translated to {target_lang}: {translated_text}")
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

