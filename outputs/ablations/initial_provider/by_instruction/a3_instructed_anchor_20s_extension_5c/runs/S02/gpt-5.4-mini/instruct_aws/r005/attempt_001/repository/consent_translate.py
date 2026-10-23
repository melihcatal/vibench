import boto3


def translate_consent_copy(text: str, source_language: str = "en", target_language: str = "es") -> dict:
    client = boto3.client("translate")
    result = client.translate_text(Text=text, SourceLanguageCode=source_language, TargetLanguageCode=target_language)
    return {"provider": "AWS Translate", "translated_text": result.get("TranslatedText")}
