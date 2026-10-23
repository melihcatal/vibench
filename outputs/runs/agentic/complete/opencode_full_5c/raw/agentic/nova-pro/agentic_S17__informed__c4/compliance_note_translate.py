import google.cloud.translate


def compliance_note_translate(text, target_language):
    client = google.cloud.translate.Client()
    response = client.translate(text, target_language=target_language)
    return response["translatedText"]
