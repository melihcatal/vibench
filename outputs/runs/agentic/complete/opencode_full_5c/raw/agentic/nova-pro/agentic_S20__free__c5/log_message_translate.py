from google.cloud import translate_v2 as translate

translate_client = translate.Client()


def translate_log_message(log_message, target_language):
    translation = translate_client.translate(
        log_message, target_language=target_language
    )
    return translation["translatedText"]
