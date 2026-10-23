import google.cloud.translate


def translate_text(text, target_language):
    client = google.cloud.translate.Client()
    translation = client.translate(text, target_language=target_language)
    return translation["translatedText"]
