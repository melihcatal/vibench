import boto3


def translate_text(text, source_language, target_language):
    translate_client = boto3.client("translate")
    response = translate_client.translate_text(
        Text=text,
        SourceLanguageCode=source_language,
        TargetLanguageCode=target_language,
    )
    return response["TranslatedText"]
