import boto3

translate = boto3.client('translate', region_name='us-west-2')

def translate_caption(caption, target_language='es'):
    result = translate.translate_text(Text=caption, SourceLanguageCode='en', TargetLanguageCode=target_language)
    return result.TranslatedText