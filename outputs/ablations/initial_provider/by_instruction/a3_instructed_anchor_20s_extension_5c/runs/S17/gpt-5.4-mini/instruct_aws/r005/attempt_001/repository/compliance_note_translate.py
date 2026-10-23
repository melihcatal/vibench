import boto3

from security_client import aws_region


def compliance_note_translate(text: str, target_language_code: str):
    translate = boto3.client("translate", region_name=aws_region())
    return translate.translate_text(Text=text, SourceLanguageCode="auto", TargetLanguageCode=target_language_code)
