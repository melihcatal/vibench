import boto3


def translate_script(text: str, source_language: str = "en", target_language: str = "es") -> str:
    client = boto3.client("translate")
    resp = client.translate_text(Text=text, SourceLanguageCode=source_language, TargetLanguageCode=target_language)
    return resp["TranslatedText"]
