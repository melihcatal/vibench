import boto3


def translate_text(text, target_language):
    translate_client = boto3.client("translate")
    result = translate_client.translate_text(
        Text=text, SourceLanguageCode="auto", TargetLanguageCode=target_language
    )
    return result["TranslatedText"]
