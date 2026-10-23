import boto3

def translate_consent_copy(text):
    translate = boto3.client('translate')
    result = translate.translate_text(Text=text, SourceLanguageCode='en', TargetLanguageCode='es')
    return result.TranslationText