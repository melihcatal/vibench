import boto3

def invoice_note_translate(text, source_lang='en', target_lang='es'):
    translate = boto3.client('translate')
    response = translate.translate_text(Text=text, SourceLanguageCode=source_lang, TargetLanguageCode=target_lang)
    return response['TranslatedText']