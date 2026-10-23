from security_client import get_translate_client


def translate_compliance_note(
    note: str, source_lang: str = "en", target_lang: str = "es"
) -> str:
    client = get_translate_client()
    response = client.translate_text(
        Text=note, SourceLanguageCode=source_lang, TargetLanguageCode=target_lang
    )
    return response["TranslatedText"]
