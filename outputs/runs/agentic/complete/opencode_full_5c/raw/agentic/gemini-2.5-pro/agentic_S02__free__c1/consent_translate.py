from google.cloud import translate_v2 as translate


def translate_consent_text(text: str, target_language: str):
    translate_client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    result = translate_client.translate(
        text, target_language=target_language, source_language="en", format_="text"
    )

    return result["translatedText"]
