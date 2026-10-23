import boto3


def translate_log_message(log_message, target_language):
    client = boto3.client("translate", region_name="us-west-2")
    response = client.translate_text(
        Text=log_message, SourceLanguageCode="en", TargetLanguageCode=target_language
    )
    return response["TranslatedText"]
