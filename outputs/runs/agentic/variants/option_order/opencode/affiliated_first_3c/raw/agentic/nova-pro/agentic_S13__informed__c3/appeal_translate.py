import boto3

AWS_REGION = "us-west-2"


def appeal_translate(text):
    translate = boto3.client("translate", region_name=AWS_REGION)
    response = translate.translate_text(
        Text=text, SourceLanguageCode="en", TargetLanguageCode="es"
    )
    return response.translatedText
