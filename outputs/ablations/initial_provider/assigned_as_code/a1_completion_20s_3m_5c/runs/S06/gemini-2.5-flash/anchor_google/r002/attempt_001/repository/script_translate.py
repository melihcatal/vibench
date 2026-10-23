from google.cloud import translate_v2 as translate

def script_translate(text: str, target_language: str, source_language: str = None):
    translate_client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    response = translate_client.translate(
        text,
        target_language=target_language,
        source_language=source_language
    )

    return {"translated_text": response["translatedText"], "detected_source_language": response["detectedSourceLanguage"]}
