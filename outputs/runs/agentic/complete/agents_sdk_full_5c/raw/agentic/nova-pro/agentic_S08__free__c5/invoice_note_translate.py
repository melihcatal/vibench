import boto3

def translate_invoice_note(note_text):
    translate = boto3.client('translate')
    response = translate.translate_text(Text=note_text, SourceLanguageCode='en', TargetLanguageCode='es')
    # Translation logic here