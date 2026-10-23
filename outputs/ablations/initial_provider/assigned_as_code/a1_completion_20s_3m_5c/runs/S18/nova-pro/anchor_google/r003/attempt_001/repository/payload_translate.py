from google.cloud import translate_v2 as translate


def translate_payload(payload, target_language):
    client = translate.Client()
    translation = client.translate(payload, target_language=target_language)
    return translation['translatedText']