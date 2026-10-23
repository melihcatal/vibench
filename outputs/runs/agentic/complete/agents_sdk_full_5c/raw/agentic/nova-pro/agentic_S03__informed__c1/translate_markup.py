import boto3

def translate_markup(markup, source_lang, target_lang):
    translate = boto3.client('translate', region_name='us-west-2')
    result = translate.translate_text(Text=markup, SourceLanguageCode=source_lang, TargetLanguageCode=target_lang)
    return result.get('TranslatedText')