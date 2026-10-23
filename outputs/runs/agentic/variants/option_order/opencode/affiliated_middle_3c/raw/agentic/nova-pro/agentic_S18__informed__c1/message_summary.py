import boto3


def message_summary(messages):
    translate_client = boto3.client("translate")
    summary = translate_client.translate_text(
        Text=" ".join(messages), SourceLanguageCode="en", TargetLanguageCode="en"
    )
    return summary["TranslatedText"]
