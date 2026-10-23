import boto3
from google.cloud import translate

translate_client = translate.Client()

s3 = boto3.client('s3')

def stored_text_translate(bucket_name, object_name, target_language='en'):
    response = s3.get_object(Bucket=bucket_name, Key=object_name)
    text_content = response['Body'].read().decode('utf-8')
    result = translate_client.translate(text_content, target_language=target_language)
    return result['translatedText']