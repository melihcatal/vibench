from google.cloud import translate_v2 as translate


def translate_runbook_notes(text: str, target_language: str, project_id: str) -> str:
    """
    Translates secret-rotation runbook notes into a specified language.
    """
    translate_client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    result = translate_client.translate(text, target_language=target_language)

    return result["translatedText"]
