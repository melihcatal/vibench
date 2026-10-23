from google.cloud import translate_v2 as translate

def translate_script(text, target_language_code, source_language_code=None):
    client = translate.Client()
    result = client.translate(text,
        target_language=target_language_code,
        source_language=source_language_code)
    return {"translated_text": result["translatedText"], "detected_source_language": result["detectedSourceLanguage"]}
