import os
import boto3

def welcome_translate(text, target_language_code):
    client = boto3.client(
        'translate',
        region_name=os.environ.get('AWS_REGION'),
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
    )

    try:
        response = client.translate_text(
            Text=text,
            SourceLanguageCode='en',
            TargetLanguageCode=target_language_code
        )
        return response['TranslatedText']
    except Exception as e:
        return {"error": str(e)}
