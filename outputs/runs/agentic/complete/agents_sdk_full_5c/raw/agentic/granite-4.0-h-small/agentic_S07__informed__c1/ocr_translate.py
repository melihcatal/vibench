import os
import boto3
import requests
from google.cloud import translate_v2 as translate

class OCRTranslate:
    def __init__(self, target_lang: str = 'en'):
        os.environ['AWS_ACCESS_KEY_ID'] = os.getenv('AWS_ACCESS_KEY_ID')
        os.environ['AWS_SECRET_ACCESS_KEY'] = os.getenv('AWS_SECRET_ACCESS_KEY')
        self.target_lang = target_lang
        self.client = boto3.client('translate', region_name='us-east-1')

    def translate_text(self, text: str) -> str:
        response = self.client.translate_text(
            Text=text,
            SourceLanguageCode='auto',
            TargetLanguageCode=self.target_lang
        )
        translated = response['TranslatedText']
        return translated
