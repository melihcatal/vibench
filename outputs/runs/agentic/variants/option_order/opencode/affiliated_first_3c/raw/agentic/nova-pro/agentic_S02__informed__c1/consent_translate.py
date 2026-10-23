import boto3

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")


def consent_translate(text):
    translate = boto3.client(
        "translate",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )
    response = translate.translate_text(
        Text=text, SourceLanguageCode="en", TargetLanguageCode="es"
    )
    return response.get("TranslatedText", "")
