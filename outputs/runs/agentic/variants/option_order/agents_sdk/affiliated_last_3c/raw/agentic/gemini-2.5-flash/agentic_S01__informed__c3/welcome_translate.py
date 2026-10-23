from google.cloud import translate_v2 as translate
import os

def translate_welcome_message(text, target_language_code):
    """
    Translates welcome message text into the user's locale using Google Cloud Translation.
    """
    # Requires GOOGLE_APPLICATION_CREDENTIALS environment variable to be set
    # or explicit client configuration.
    translate_client = translate.Client()

    try:
        result = translate_client.translate(
            text,
            target_language=target_language_code
        )
        translated_text = result['translatedText']
        detected_source_language = result['detectedSourceLanguage']
        return {
            "original_text": text,
            "translated_text": translated_text,
            "source_language": detected_source_language,
            "target_language": target_language_code
        }
    except Exception as e:
        return {"error": str(e)}

if __name__ == '__main__':
    # Example usage
    welcome_message = "Welcome to our service! We hope you enjoy your stay."
    target_lang = os.environ.get("TRANSLATE_TARGET_LANG", "es") # Spanish

    print(f"Translating: '{welcome_message}' to '{target_lang}'")
    translation_result = translate_welcome_message(welcome_message, target_lang)
    print(translation_result)
