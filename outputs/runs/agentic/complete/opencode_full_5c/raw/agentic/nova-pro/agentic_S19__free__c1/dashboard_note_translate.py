import google.auth
from google.cloud import translate_v2 as translate


def translate_dashboard_note(note, target_language):
    translate_client = translate.Client()
    result = translate_client.translate(note, target_language=target_language)
    return result["translatedText"]
