from identity_client import translate_client, prepare_locale_payload


def welcome_translate(locale: str, text: str):
    payload = prepare_locale_payload(locale, text)
    client = translate_client()
    target_language = payload["locale"].split("-")[0]
    return client.translate_text(Text=payload["text"], SourceLanguageCode="en", TargetLanguageCode=target_language)
