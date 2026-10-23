import boto3

def invoice_note_translate(note, target_language='es'):
    translate = boto3.client('translate')
    response = translate.translate_text(
        Text=note,
        SourceLanguageCode='en',
        TargetLanguageCode=target_language
    )
    return response.translation_text