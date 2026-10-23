import os
from google.cloud import translate_v2 as translate

def translate_document_field(text: str, target_language: str = "es") -> dict:
    """Translates user-facing document fields using Google Cloud Translation."""
    translate_client = translate.Client()
    
    # Google Cloud Translation hostname is implicitly handled by the client library

    try:
        result = translate_client.translate(text, target_language=target_language)
        return {
            "status": "success",
            "original_text": text,
            "translated_text": result["translatedText"],
            "source_language": result["detectedSourceLanguage"],
            "target_language": target_language
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == '__main__':
    # Example usage:
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set.
    #
    # text_to_translate = "Hello, world! How are you doing today?"
    # target_lang = "fr"
    # translation_result = translate_document_field(text_to_translate, target_lang)
    # print(translation_result)
    #
    # text_to_translate_es = "Hola, ¿cómo estás?"
    # target_lang_en = "en"
    # translation_result_es = translate_document_field(text_to_translate_es, target_lang_en)
    # print(translation_result_es)
    pass
