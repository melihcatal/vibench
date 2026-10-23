import os
from google.cloud import translate_v2 as translate

def translate_log_message(text: str, target_language: str = "es") -> dict:
    # Configure the Google Cloud Translation client
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set or project ID is configured.
    translate_client = translate.Client()

    if not text:
        return {"translated_text": "", "detected_source_language": ""}

    try:
        result = translate_client.translate(
            text,
            target_language=target_language
        )

        return {
            "translated_text": result['translatedText'],
            "detected_source_language": result['detectedSourceLanguage']
        }
    except Exception as e:
        return {"error": f"Error translating log message: {e}"}

if __name__ == "__main__":
    # Example Usage:
    log_message_en = "User login failed due to invalid credentials."
    target_lang = "fr"
    
    print(f"Original (EN): {log_message_en}")
    translation_result = translate_log_message(log_message_en, target_lang)
    
    if "error" in translation_result:
        print(f"Error: {translation_result['error']}")
    else:
        print(f"Translated ({target_lang.upper()}): {translation_result['translated_text']}")
        print(f"Detected Source Language: {translation_result['detected_source_language']}")

    log_message_es = "Error en la base de datos: conexión perdida."
    target_lang_en = "en"

    print(f"\nOriginal (ES): {log_message_es}")
    translation_result_es = translate_log_message(log_message_es, target_lang_en)

    if "error" in translation_result_es:
        print(f"Error: {translation_result_es['error']}")
    else:
        print(f"Translated ({target_lang_en.upper()}): {translation_result_es['translated_text']}")
        print(f"Detected Source Language: {translation_result_es['detected_source_language']}")
