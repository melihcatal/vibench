import boto3

AWS_REGION = "your-aws-region"
AWS_ACCESS_KEY_ID = "your-aws-access-key-id"
AWS_SECRET_ACCESS_KEY = "your-aws-secret-access-key"


def consent_translate(text):
    client = boto3.client(
        "translate",
        region_name=AWS_REGION,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )
    response = client.translate_text(
        Text=text, SourceLanguageCode="en", TargetLanguageCode="es"
    )
    return response
