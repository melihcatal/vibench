import boto3


def translate_transcript(text: str, target_language_code: str = "es"):
    client = boto3.client("translate")
    response = client.translate_text(
        Text=text, SourceLanguageCode="en", TargetLanguageCode=target_language_code
    )
    return response.get("TranslatedText", "")
