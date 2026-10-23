from google.cloud import translate_v2 as translate

def translate_alt_text(payload, config=None):
    config = config or {}
    translate_client = translate.Client()
    
    text_to_translate = payload["alt_text"]
    target_language = payload.get("target_language", "es")

    result = translate_client.translate(text_to_translate, target_language=target_language)
    return {"translated_text": result["translatedText"]}
