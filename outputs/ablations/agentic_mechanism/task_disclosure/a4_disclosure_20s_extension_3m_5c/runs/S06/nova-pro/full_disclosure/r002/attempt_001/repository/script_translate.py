import boto3

def translate_script(script, target_language):
    translate = boto3.client('translate')
    result = translate.translate_text(Text=script, SourceLanguageCode='auto', TargetLanguageCode=target_language)
    return result.TranslatedText