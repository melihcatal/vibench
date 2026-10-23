import boto3

def translate_text(text):
    translate = boto3.client('translate')
    result = translate.translate_text(Text=text, SourceLanguageCode='auto', TargetLanguageCode='en')
    return result.TranslatedText

if __name__ == '__main__':
    invoice_note = 'Sample invoice note to be translated.'
    translated_note = translate_text(invoice_note)
    print(f'Translated note: {translated_note}')
