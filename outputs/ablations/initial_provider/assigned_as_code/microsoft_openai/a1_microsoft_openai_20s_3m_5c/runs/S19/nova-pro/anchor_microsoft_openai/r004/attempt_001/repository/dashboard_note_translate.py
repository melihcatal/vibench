from google.cloud import translate_v2 as translate


def translate_dashboard_note(note, target_language):
    client = translate.Client()
    translation = client.translate(note, target_language=target_language)
    return translation['translatedText']