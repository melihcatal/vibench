from google.cloud import translate_v2 as translate


def alt_text_translate(description: str, target_language: str = "es") -> str:
    client = translate.Client()
    if isinstance(description, list):
        description = " ".join(description)
    result = client.translate(description, target_language=target_language)
    return result["translatedText"]
