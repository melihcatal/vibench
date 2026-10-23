import boto3


def translate_invoice_note(note, target_language='es'):
    translate = boto3.client('translate')
    response = translate.translate_text(Text=note, SourceLanguageCode='en', TargetLanguageCode=target_language)
    return response.get('TranslatedText')