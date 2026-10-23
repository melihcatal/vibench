import boto3

from storage_models import normalize_text


def stored_text_translate(text, target_language_code: str = "en"):
    translate = boto3.client("translate")
    response = translate.translate_text(Text=normalize_text(text), SourceLanguageCode="auto", TargetLanguageCode=target_language_code)
    return response.get("TranslatedText", "")
