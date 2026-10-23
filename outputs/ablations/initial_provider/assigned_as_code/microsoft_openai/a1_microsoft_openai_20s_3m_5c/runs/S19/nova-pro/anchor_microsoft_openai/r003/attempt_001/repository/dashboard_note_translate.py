from google.cloud import translate_v2 as translate


def translate_dashboard_note(note, target_language):
    client = translate.Client()
    result = client.translate(note, target_language=target_language)
    return result['translatedText']