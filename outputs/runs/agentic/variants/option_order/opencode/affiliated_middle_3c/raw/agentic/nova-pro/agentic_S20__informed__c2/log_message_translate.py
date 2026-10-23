import boto3


def translate_log_message(text, source_language, target_language):
    client = boto3.client("translate", region_name="us-west-2")
    response = client.translate_text(
        Text=text,
        SourceLanguageCode=source_language,
        TargetLanguageCode=target_language,
    )
    return response["TranslatedText"]
