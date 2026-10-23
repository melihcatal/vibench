import boto3
from botocore.exceptions import ClientError


def translate_text(text, source_language_code, target_language_code):
    translate_client = boto3.client('translate', region_name='your-region')
    try:
        response = translate_client.translate_text(
            Text=text,
            SourceLanguageCode=source_language_code,
            TargetLanguageCode=target_language_code
        )
    except ClientError as e:
        raise e
    return response