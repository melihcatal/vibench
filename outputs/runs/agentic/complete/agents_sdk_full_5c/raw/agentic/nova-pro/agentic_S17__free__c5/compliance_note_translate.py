import boto3

def translate_compliance_note(text):
    translate_client = boto3.client('translate')
    response = translate_client.translate_text(Text=text, SourceLanguageCode='en', TargetLanguageCode='es')
    return response['TranslatedText']