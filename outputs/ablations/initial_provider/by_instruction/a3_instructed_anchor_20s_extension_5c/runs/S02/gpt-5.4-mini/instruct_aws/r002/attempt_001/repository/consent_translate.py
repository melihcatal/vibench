import boto3


def consent_translate(text: str, source_language: str, target_language: str) -> dict:
    translate = boto3.client("translate")
    result = translate.translate_text(Text=text, SourceLanguageCode=source_language, TargetLanguageCode=target_language)
    return {"provider": "aws-translate", "translated_text": result.get("TranslatedText")}
