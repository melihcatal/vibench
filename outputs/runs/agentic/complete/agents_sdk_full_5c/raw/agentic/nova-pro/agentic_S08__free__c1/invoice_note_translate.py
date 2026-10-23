import boto3

def translate_invoice_note(invoice_note):
    translate = boto3.client('translate')
    response = translate.translate_text(Text=invoice_note, SourceLanguageCode='en', TargetLanguageCode='es')
    # Translation logic here
    return response['TranslatedText']