import boto3


def translate_transcript(text: str, target_language_code: str):
    client = boto3.client("translate")
    resp = client.translate_text(Text=text, SourceLanguageCode="auto", TargetLanguageCode=target_language_code)
    return resp.get("TranslatedText", "")
