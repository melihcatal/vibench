import google.cloud.translate


def translate_script(script, target_language):
    client = google.cloud.translate.Client()
    result = client.translate(script, target_language=target_language)
    return result['translatedText']