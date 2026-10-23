import boto3

translate = boto3.client('translate', region_name='us-west-2', aws_access_key_id='YOUR_ACCESS_KEY', aws_secret_access_key='YOUR_SECRET_KEY')

def translate_text(text, target_language='es'):
    result = translate.translate_text(Text=text, SourceLanguageCode='en', TargetLanguageCode=target_language)
    return result.get('TranslatedText')
