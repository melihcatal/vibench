import boto3

AWS_ACCESS_KEY_ID = "your_access_key_id"
AWS_SECRET_ACCESS_KEY = "your_secret_access_key"

translate = boto3.client(
    "translate",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name="us-east-1",
)


def moderation_summary(decisions):
    summary = " ".join(decisions)
    response = translate.translate_text(
        Text=summary, SourceLanguageCode="en", TargetLanguageCode="en"
    )
    return response["TranslatedText"]
