from google.cloud import translate_v2 as translate
import os

def welcome_translate(text: str, target_language: str, source_language: Optional[str] = None) -> dict:
    # Initialize the Google Cloud Translation client
    # Requires GOOGLE_APPLICATION_CREDENTIALS to be set
    translate_client = translate.Client()

    try:
        result = translate_client.translate(
            text,
            target_language=target_language,
            source_language=source_language
        )
        return {
            "original_text": text,
            "translated_text": result["translatedText"],
            "source_language": result["detectedSourceLanguage"]
        }
    except Exception as e:
        raise RuntimeError(f"Failed to translate text: {e}")

if __name__ == '__main__':
    # Example usage (requires GOOGLE_APPLICATION_CREDENTIALS to be set)
    # import os
    # os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "/path/to/your/service-account-key.json"
    # try:
    #     translated_message = welcome_translate("Welcome to our service!", "es")
    #     print(f"Translated welcome message: {translated_message}")
    #     translated_message_fr = welcome_translate("Hello there!", "fr", "en")
    #     print(f"Translated greeting: {translated_message_fr}")
    # except RuntimeError as e:
    #     print(f"Error: {e}")
    pass
