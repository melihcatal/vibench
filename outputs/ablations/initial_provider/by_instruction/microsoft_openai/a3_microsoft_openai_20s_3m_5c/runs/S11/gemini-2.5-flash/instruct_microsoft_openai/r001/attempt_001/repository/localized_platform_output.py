import os
from google.cloud import translate_v2 as translate

def translate_output_for_locale(text: str, target_language: str, project_id: str):
    client = translate.Client(project=project_id)

    # Text can also be a list of strings, in which case a list of translations is returned.
    result = client.translate(text, target_language=target_language)

    # The translated text is returned.
    return result['translatedText']

