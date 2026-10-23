from google.cloud import translate_v2 as translate


def translate_text(text: str, source_lang: str = "en", target_lang: str = "es") -> str:
    client = translate.Client()
    result = client.translate(
        text,
        source_language=source_lang if source_lang != "auto" else None,
        target_language=target_lang,
    )
    return result["translatedText"]
