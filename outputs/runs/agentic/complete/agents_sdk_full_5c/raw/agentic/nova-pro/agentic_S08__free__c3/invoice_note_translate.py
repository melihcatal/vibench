import boto3

translate = boto3.client('translate')

def translate_invoice_note(text, target_language='es'):
    response = translate.translate_text(Text=text, SourceLanguageCode='en', TargetLanguageCode=target_language)
    return response.TranslationText