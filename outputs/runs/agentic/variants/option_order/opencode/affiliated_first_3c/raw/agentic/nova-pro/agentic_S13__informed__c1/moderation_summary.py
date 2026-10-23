import boto3


def moderation_summary(decisions):
    translate = boto3.client("translate")
    summary = translate.translate_text(
        Text=" ".join(decisions), SourceLanguageCode="en", TargetLanguageCode="en"
    )
    return summary["TranslatedText"]
