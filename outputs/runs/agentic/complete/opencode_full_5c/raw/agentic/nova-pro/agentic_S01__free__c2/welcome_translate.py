import google.cloud.translate


def translate_text(text, target_language):
    translate_client = google.cloud.translate.Client()
    result = translate_client.translate(text, target_language=target_language)
    return result["translatedText"]
