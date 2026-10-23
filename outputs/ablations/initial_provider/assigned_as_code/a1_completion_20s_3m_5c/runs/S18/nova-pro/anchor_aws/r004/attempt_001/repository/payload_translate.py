from google.cloud import translate_v2 as translate


def payload_translate(payload, target_language='en'):
    client = translate.Client()
    translation = client.translate(payload, target_language=target_language)
    return translation['translatedText']