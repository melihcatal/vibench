import boto3

translate_client = boto3.client("translate")


def dashboard_note_translate(note: str, source_lang: str, target_lang: str):
    response = translate_client.translate_text(
        Text=note, SourceLanguageCode=source_lang, TargetLanguageCode=target_lang
    )
    return response["TranslatedText"]
