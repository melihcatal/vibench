import boto3

s3 = boto3.client('s3', region_name='us-west-2')

def translate_text(text, source_language_code, target_language_code):
    translate = boto3.client('translate', region_name='us-west-2')
    result = translate.translate_text(Text=text, SourceLanguageCode=source_language_code, TargetLanguageCode=target_language_code)
    return result.translationText