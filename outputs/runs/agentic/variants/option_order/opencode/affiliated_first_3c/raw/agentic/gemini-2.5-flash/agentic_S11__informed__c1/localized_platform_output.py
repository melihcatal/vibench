from google.cloud import translate_v2 as translate
import os


def translate_output(text: str, target_language: str, project_id: str) -> dict:
    client = translate.Client(project=project_id)
    result = client.translate(text, target_language=target_language)
    return result
