"""[LATER-STEP] Translate generated image descriptions"""
import boto3

def alt_text_translate(text: str, target_lang: str = 'es') -> str:
    # Amazon Translate
    translate = boto3.client('translate')
    response = translate.translate_text(
        Text=text,
        SourceLanguageCode='en',
        TargetLanguageCode=target_lang
    )
    return response['TranslatedText']
