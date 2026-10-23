import google.auth
from google.cloud import translate_v2 as translate


def translate_script(script, target_language):
    credentials, project = google.auth.default()
    translate_client = translate.Client(credentials=credentials, project=project)
    result = translate_client.translate(script, target_language=target_language)
    return result["translatedText"]