from google.cloud import translate_v2 as translate


def stored_text_translate(text: str, target_language: str = "en"):
    client = translate.Client()
    return client.translate(text, target_language=target_language)
