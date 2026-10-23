import os
from google.cloud import translate_v2 as translate

def translate_text_content(text: str, target_language: str = "es") -> str:
    translate_client = translate.Client()
    result = translate_client.translate(text, target_language=target_language)
    return result['translatedText']

def runbook_translate(runbook_note: str, target_language: str = "es") -> str:
    return translate_text_content(runbook_note, target_language)

if __name__ == '__main__':
    sample_runbook_note = "Rotate the API key every 90 days as per security policy."
    # translated_note = runbook_translate(sample_runbook_note, "fr")
    # print(f"Original: {sample_runbook_note}")
    # print(f"Translated (French): {translated_note}")
