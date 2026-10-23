from document_client import translate_client, load_config


def invoice_note_translate(text):
    client = translate_client()
    config = load_config()
    response = client.translate_text(
        Text=text,
        SourceLanguageCode=config.translate_source_lang,
        TargetLanguageCode=config.translate_target_lang,
    )
    return {
        "translated_text": response.get("TranslatedText", ""),
        "provider": "aws-translate",
    }
