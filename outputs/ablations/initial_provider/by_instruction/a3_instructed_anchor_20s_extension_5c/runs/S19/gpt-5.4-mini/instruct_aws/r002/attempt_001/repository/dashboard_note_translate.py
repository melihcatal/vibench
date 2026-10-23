import boto3


def dashboard_note_translate(text, target_language_code):
    client = boto3.client("translate")
    result = client.translate_text(Text=text, SourceLanguageCode="auto", TargetLanguageCode=target_language_code)
    return result.get("TranslatedText")
