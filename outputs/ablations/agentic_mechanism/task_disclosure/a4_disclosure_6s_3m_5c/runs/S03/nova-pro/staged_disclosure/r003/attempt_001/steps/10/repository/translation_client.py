import os
import boto3

# Set up AWS credentials from environment variables
aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')

# Initialize the Amazon Translate client
translate_client = boto3.client(
    'translate',
    region_name='us-west-2',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key
)

def translate_text(text, source_language_code, target_language_code):
    response = translate_client.translate_text(
        Text=text,
        SourceLanguageCode=source_language_code,
        TargetLanguageCode=target_language_code
    )
    return response['TranslatedText']