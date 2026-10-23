import boto3

AWS_ACCESS_KEY_ID = "your_access_key_id"
AWS_SECRET_ACCESS_KEY = "your_secret_access_key"

translate = boto3.client(
    "translate",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name="us-east-1",
)


def appeal_translate(text):
    response = translate.translate_text(
        Text=text, SourceLanguageCode="en", TargetLanguageCode="en"
    )
    return response["TranslatedText"]
