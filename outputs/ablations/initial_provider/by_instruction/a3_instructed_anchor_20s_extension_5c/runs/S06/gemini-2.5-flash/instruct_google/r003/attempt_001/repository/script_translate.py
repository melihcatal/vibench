from google.cloud import translate_v2 as translate

def translate_script(text: str, target_language: str) -> str:
    """
    Translates narration scripts using Google Cloud Translation API.
    """
    translate_client = translate.Client()

    result = translate_client.translate(text, target_language=target_language)

    return result["translatedText"]
