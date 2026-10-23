import boto3
import translate

from storage_client import get_s3_client


def translate_stored_text(object_name, target_language='es'):
    client = get_s3_client()
    response = client.get_object(Bucket='your-bucket-name', Key=object_name)
    text = response['Body'].read().decode('utf-8')
    translator = translate.Translator(to_lang=target_language)
    translated_text = translator.translate(text)
    return translated_text