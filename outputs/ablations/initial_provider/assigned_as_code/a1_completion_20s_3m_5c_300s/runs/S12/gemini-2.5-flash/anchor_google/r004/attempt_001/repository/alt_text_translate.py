from google.cloud import translate_v2 as translate

def alt_text_translate(payload, config=None):
    config = config or {}
    translate_client = translate.Client()

    text_to_translate = payload["text"]
    target_language = config.get("target_language", "en")

    result = translate_client.translate(text_to_translate, target_language=target_language)
    
    return {"translated_text": result["translatedText"], "original_text": result["input"], "source_language": result["detectedSourceLanguage"]}
