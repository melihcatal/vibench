from google.cloud import translate_v2 as translate


def translate_invoice_note(text: str, target_language: str = "en") -> str:
    """Translates text into the target language.

    Target langauges must be ISO 639-1 language codes.
    See https://g.co/cloud/translate/v2/translate-reference/languages
    """
    translate_client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    result = translate_client.translate(text, target_language=target_language)

    return result["translatedText"]
