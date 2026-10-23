from google.cloud import translate_v2 as translate


def translate_log_message(log_message, target_language):
    translate_client = translate.Client()
    translation = translate_client.translate(log_message, target_language=target_language)
    return translation['translatedText']