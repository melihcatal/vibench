from google.cloud import translate_v2 as translate
import os
from observability_models import TranslationRequest, TranslationResponse

def translate_log_message(request: TranslationRequest) -> TranslationResponse:
    """
    Translates support-visible log messages for another locale using Google Cloud Translation API.

    Args:
        request: A TranslationRequest object containing the text to translate, target language,
                 and optional source language.

    Returns:
        A TranslationResponse object with the translated text and detected source language.
    """
    client = translate.Client()

    # The target language is required
    if not request.target_language:
        raise ValueError("Target language must be provided for translation.")

    result = client.translate(
        request.text,
        target_language=request.target_language,
        source_language=request.source_language # Optional, will be auto-detected if not provided
    )

    translated_text = result['translatedText']
    detected_source_language = result['detectedSourceLanguage'] if 'detectedSourceLanguage' in result else None

    return TranslationResponse(translated_text=translated_text, detected_source_language=detected_source_language)

if __name__ == "__main__":
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set or
    # your environment is otherwise authenticated for Google Cloud Translation API.

    print("\n--- Translation Example 1 (English to Spanish) ---")
    en_to_es_request = TranslationRequest(
        text="User login failed due to incorrect password attempt.",
        target_language="es"
    )
    try:
        es_response = translate_log_message(en_to_es_request)
        print(f"Original: \"{en_to_es_request.text}\"")
        print(f"Translated (es): \"{es_response.translated_text}\"")
        print(f"Detected Source Language: {es_response.detected_source_language}")
    except Exception as e:
        print(f"Error translating: {e}")

    print("\n--- Translation Example 2 (Auto-detect to German) ---")
    auto_to_de_request = TranslationRequest(
        text="La base de datos no responde, por favor revise la conexión.",
        target_language="de"
    )
    try:
        de_response = translate_log_message(auto_to_de_request)
        print(f"Original: \"{auto_to_de_request.text}\"")
        print(f"Translated (de): \"{de_response.translated_text}\"")
        print(f"Detected Source Language: {de_response.detected_source_language}")
    except Exception as e:
        print(f"Error translating: {e}")
