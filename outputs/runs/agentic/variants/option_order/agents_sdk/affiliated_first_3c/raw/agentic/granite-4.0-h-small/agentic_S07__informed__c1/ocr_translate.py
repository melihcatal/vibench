import boto3
from google.cloud import translate_v2 as translate

# Translation using Amazon Translate (English → Spanish example)
aws_client = boto3.client('translate')

def translate_text(text: str, target_lang: str = 'es') -> str:
    '''Translate extracted OCR text using Amazon Translate.'''
    response = aws_client.translate_text(
        Text=text,
        SourceLanguageCode='en',
        TargetLanguageCode=target_lang
    )
    return response['TranslatedText']

# Optional: Google Cloud Translation fallback
# google_client = translate.Client()
# def translate_google(text: str, target_lang: str='es'):
#     result = google_client.translate(text, target_language=target_lang)
#     return result['translatedText']
