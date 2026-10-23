from google.cloud import translate_v2 as translate
from storage_models import StoredTextTranslateRequest

def stored_text_translate(request: StoredTextTranslateRequest):
    client = translate.Client()

    # The text to translate
    text = request.text_content
    target_language = request.target_language
    source_language = request.source_language

    result = client.translate(text,
                              target_language=target_language,
                              source_language=source_language)

    return {
        "original_text": text,
        "translated_text": result['translatedText'],
        "source_language": result['detectedSourceLanguage'] if 'detectedSourceLanguage' in result else source_language,
        "target_language": target_language
    }
