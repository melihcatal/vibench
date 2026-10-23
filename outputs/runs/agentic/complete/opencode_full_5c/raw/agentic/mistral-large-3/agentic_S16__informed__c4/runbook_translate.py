from google.cloud import translate_v2 as translate
import os


def runbook_translate(runbook_text: str, target_language: str = "es") -> str:
    client = translate.Client()

    if not isinstance(runbook_text, str):
        raise ValueError("Runbook text must be a string")

    result = client.translate(runbook_text, target_language=target_language)
    return result["translatedText"]
