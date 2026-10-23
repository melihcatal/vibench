import boto3
from botocore.exceptions import NoCredentialsError

def translate_text(text, target_language='es'):
    client = boto3.client('translate')
    try:
        result = client.translate_text(Text=text, SourceLanguageCode='auto', TargetLanguageCode=target_language)
        return result['TranslatedText']
    except NoCredentialsError:
        raise Exception('AWS credentials not found')