from google.cloud import translate_v2 as translate
from security_client import get_gcp_translate_project


def translate_secret_rotation_runbook(notes: str, target_language: str = "en") -> str:
    project = get_gcp_translate_project()
    client = translate.Client(project=project)
    result = client.translate(notes, target_language=target_language)
    return result["translatedText"]
