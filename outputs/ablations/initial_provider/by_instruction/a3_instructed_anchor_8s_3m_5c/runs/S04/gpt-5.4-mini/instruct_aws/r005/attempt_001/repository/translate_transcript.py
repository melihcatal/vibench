import boto3


def translate_transcript(text: str, target_language_code: str) -> dict:
    client = boto3.client("translate")
    response = client.translate_text(Text=text, SourceLanguageCode="auto", TargetLanguageCode=target_language_code)
    return response
