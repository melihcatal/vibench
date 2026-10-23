from google.cloud import translate_v2 as translate

def translate_stored_text(payload, config=None):
    config = config or {}
    client = translate.Client()
    
    text_to_translate = payload.get("text")
    target_language = payload.get("target_language", "en")

    if not text_to_translate:
        raise ValueError("Text to translate must be provided.")

    result = client.translate(text_to_translate, target_language=target_language)
    
    return {"translated_text": result["translatedText"], "source_language": result["detectedSourceLanguage"]}
