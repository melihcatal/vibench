import os
import boto3

def translate_log_message(text, target_language):
    translate = boto3.client('translate')
    response = translate.translate_text(
        Text=text,
        SourceLanguageCode='en',
        TargetLanguageCode=target_language
    )
    return response['TranslatedText']
