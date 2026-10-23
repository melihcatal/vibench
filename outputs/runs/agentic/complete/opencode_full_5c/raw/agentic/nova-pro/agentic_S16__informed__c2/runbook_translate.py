import boto3

client = boto3.client("translate")


def runbook_translate(text, source_language, target_language):
    response = client.translate_text(
        Text=text,
        SourceLanguageCode=source_language,
        TargetLanguageCode=target_language,
    )
    return response["TranslatedText"]
