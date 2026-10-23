import boto3

def translate_text(text):
    translate = boto3.client('translate')
    result = translate.translate_text(Text=text, SourceLanguageCode='en', TargetLanguageCode='es')
    return result.get('TranslatedText')