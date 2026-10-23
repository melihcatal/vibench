from google.cloud import translate_v2 as translate


def record_translate(document, target_language):
    translate_client = translate.Client()
    translated_document = {}
    for key, value in document.items():
        if isinstance(value, str):
            translation = translate_client.translate(value, target_language=target_language)
            translated_document[key] = translation["translatedText"]
        else:
            translated_document[key] = value
    return translated_document