import boto3

def translate_markup(markup_text, source_language, target_language):
    translate = boto3.client('translate', region_name='us-west-2')
    result = translate.translate_text(Text=markup_text, SourceLanguageCode=source_language, TargetLanguageCode=target_language)
    return result.translationText