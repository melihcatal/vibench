import boto3

def translate_compliance_note(note):
    translate = boto3.client('translate')
    result = translate.translate_text(Text=note, SourceLanguageCode='en', TargetLanguageCode='es')
    return result.get('TranslatedText')

if __name__ == '__main__':
    sample_note = 'This is a sample compliance note.'
    translated_note = translate_compliance_note(sample_note)
    print(f'Translated Note: {translated_note}')