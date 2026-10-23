import boto3
import os

def translate_appeal_text_aws(text: str, source_language: str = 'auto', target_language: str = 'en') -> str:
    """
    Translates appeal text for review using AWS Translate.
    """
    translate = boto3.client(
        'translate',
        region_name=os.environ.get('AWS_REGION', 'us-east-1'),
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
    )

    if source_language == 'auto':
        response = translate.translate_text(
            Text=text,
            SourceLanguageCode='auto',
            TargetLanguageCode=target_language
        )
    else:
        response = translate.translate_text(
            Text=text,
            SourceLanguageCode=source_language,
            TargetLanguageCode=target_language
        )

    return response['TranslatedText']
