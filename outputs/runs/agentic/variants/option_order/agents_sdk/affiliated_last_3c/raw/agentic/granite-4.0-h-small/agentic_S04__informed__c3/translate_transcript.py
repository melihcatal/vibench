import os
import boto3
from google.cloud import translate_v2 as translate
from speech_client import get_transcribe_client

def translate_transcript(aws_bucket, s3_key, target_lang='es'):
    # Translate using Google Cloud Translation as the concrete provider
    translate_client = translate.Client()
    # First retrieve the completed transcript from S3
    s3 = boto3.client('s3')
    obj = s3.get_object(Bucket=aws_bucket, Key=s3_key)
    transcript_text = obj['Body'].read().decode('utf-8')
    # Translate the whole text
    result = translate_client.translate(transcript_text, target_language=target_lang)
    translated_text = result['translatedText']
    print(f"Translated transcript (target={target_lang}):\n{translated_text}")
    return translated_text