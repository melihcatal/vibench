from google.cloud import translate_v2 as translate
import os

def translate_script(text: str, target_language: str, project_id: str = None) -> str:
    translate_client = translate.Client(project=project_id)

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text. (The `text` parameter can
    # also be a list of strings.)
    result = translate_client.translate(text, target_language=target_language)

    return result["translatedText"]
