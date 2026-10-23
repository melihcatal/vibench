import boto3
import os

class TranslationClient:
    def __init__(self):
        self.client = boto3.client(
            'translate',
            region_name=os.environ.get('AWS_REGION', 'us-east-1'),
            aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
        )

    def translate_text(self, text: str, source_language: str, target_language: str) -> str:
        response = self.client.translate_text(
            Text=text,
            SourceLanguageCode=source_language,
            TargetLanguageCode=target_language
        )
        return response['TranslatedText']

    def batch_translate_text(self, texts: list[str], source_language: str, target_language: str) -> list[str]:
        # AWS Translate doesn't have a direct batch translate_text API for a list of strings
        # We will simulate it by translating each text individually
        translated_texts = []
        for text in texts:
            translated_texts.append(self.translate_text(text, source_language, target_language))
        return translated_texts
