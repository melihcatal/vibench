import os
import boto3

translate_client = boto3.client('translate')

def translate_consent(text, target_language):
    response = translate_client.translate_text(
        Text=text,
        SourceLanguageCode='en',
        TargetLanguageCode=target_language
    )
    print(response['TranslatedText'])

if __name__ == '__main__':
    translate_consent('example consent text', 'es')