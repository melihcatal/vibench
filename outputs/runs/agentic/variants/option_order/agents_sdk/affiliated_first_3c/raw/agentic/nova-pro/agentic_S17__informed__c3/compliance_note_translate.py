import boto3

def translate_compliance_note(text):
    translate = boto3.client('translate')
    response = translate.translate_text(Text=text, SourceLanguageCode='en', TargetLanguageCode='en')
    return response['TranslatedText']