import boto3
from observability_client import create_cw_client

cw_client = create_cw_client()
translate_client = boto3.client("translate")


def dashboard_note_translate(note, source_lang, target_lang):
    response = translate_client.translate_text(
        Text=note, SourceLanguageCode=source_lang, TargetLanguageCode=target_lang
    )
    return response["TranslatedText"]
