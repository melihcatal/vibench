from google.cloud import translate_v2 as translate


def translate_payload(payload, target_language='en'):
    translate_client = translate.Client()
    translated_payload = translate_client.translate(payload, target_language=target_language)
    return translated_payload['translatedText']