from google.cloud import translate_v2 as translate


def translate_appeal_text(text: str, target_language: str = "en") -> str:
    """
    Translates appeal text to a target language using Google Cloud Translation.
    """
    translate_client = translate.Client()

    result = translate_client.translate(text, target_language=target_language)

    return result["translatedText"]
