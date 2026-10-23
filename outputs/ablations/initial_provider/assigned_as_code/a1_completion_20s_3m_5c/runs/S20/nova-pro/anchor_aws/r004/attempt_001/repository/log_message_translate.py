from google.cloud import translate_v2 as translate


def translate_log_message(message, target_language):
    client = translate.Client()
    translation = client.translate(message, target_language=target_language)
    return translation["translatedText"]