from google.cloud import translate_v2 as translate

def log_message_translate(log_text, target_language):
    client = translate.Client()
    result = client.translate(log_text, target_language=target_language)
    return result["translatedText"]