import boto3
from model_client import aws_region


def localized_platform_output(text, target_locale="es"):
    client = boto3.client("translate", region_name=aws_region())
    return client.translate_text(Text=text, SourceLanguageCode="en", TargetLanguageCode=target_locale)
