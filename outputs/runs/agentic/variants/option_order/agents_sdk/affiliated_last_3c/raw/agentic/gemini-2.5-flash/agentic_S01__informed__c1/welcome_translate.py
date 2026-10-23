import os
from google.cloud import translate_v2 as translate

def welcome_translate(text: str, target_language: str) -> dict:
    # GOOGLE_APPLICATION_CREDENTIALS environment variable must be set
    translate_client = translate.Client()

    try:
        result = translate_client.translate(text, target_language=target_language)
        return {
            "translated_text": result["translatedText"],
            "detected_source_language": result["detectedSourceLanguage"],
            "input_text": result["input"]
        }
    except Exception as e:
        return {"error": str(e)}

if __name__ == '__main__':
    # Example usage (requires GOOGLE_APPLICATION_CREDENTIALS to be set)
    # translated_welcome = welcome_translate("Welcome to our service!", "es")
    # print(translated_welcome)
    pass
