import boto3


def dashboard_note_translate(text: str, target_language_code: str) -> str:
    client = boto3.client("translate")
    response = client.translate_text(
        Text=text, SourceLanguageCode="auto", TargetLanguageCode=target_language_code
    )
    return response.get("TranslatedText", "")
