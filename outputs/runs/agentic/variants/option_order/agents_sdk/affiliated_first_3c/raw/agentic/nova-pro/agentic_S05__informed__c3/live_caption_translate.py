import boto3
from botocore.exceptions import NoCredentialsError

translate = boto3.client('translate', region_name='us-west-2')

def translate_caption(caption, target_language):
    try:
        response = translate.translate_text(
            Text=caption,
            SourceLanguageCode='en',
            TargetLanguageCode=target_language,
        )
        return response['TranslatedText']
    except NoCredentialsError:
        print('No AWS credentials found')