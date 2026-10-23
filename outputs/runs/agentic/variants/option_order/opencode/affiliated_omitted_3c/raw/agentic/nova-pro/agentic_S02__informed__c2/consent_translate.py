import google.cloud.translate


# Translate identity-provider consent copy
def translate_consent(text, target_language):
    client = google.cloud.translate.Client()
    result = client.translate(text, target_language=target_language)
    return result["translatedText"]
