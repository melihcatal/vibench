import boto3

def translate_text(text, source_lang, target_lang):
    translate = boto3.client('translate')
    result = translate.translate_text(Text=text, SourceLanguageCode=source_lang, TargetLanguageCode=target_lang)
    return result.TranslatedText

if __name__ == '__main__':
    invoice_note = 'Sample invoice note to be translated.'
    source_language = 'en'
    target_language = 'es'
    translated_note = translate_text(invoice_note, source_language, target_language)
    print(f'Translated Note: {translated_note}')
