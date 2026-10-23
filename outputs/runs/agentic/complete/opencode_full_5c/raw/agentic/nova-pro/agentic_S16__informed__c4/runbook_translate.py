from google.cloud import translate_v2 as translate


def translate_runbook_notes(notes):
    client = translate.Client()
    response = client.translate(notes, target_language="en")
    return response["translatedText"]
