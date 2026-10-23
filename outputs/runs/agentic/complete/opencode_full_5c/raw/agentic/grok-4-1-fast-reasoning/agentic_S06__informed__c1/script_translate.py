from google.cloud import translate_v2 as translate
import os


def translate_script(script: str, target_language: str = "es") -> str:
    client = translate.Client()
    if isinstance(script, list):
        script = " ".join(script)
    result = client.translate(script, target_language=target_language)
    return result["translatedText"]
