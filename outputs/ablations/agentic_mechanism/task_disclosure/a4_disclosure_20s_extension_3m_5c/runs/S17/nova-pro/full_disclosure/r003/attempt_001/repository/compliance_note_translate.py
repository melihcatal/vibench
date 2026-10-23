from google.cloud import translate_v2 as translate

def translate_compliance_note(note, target_language='en'):
    client = translate.Client()
    result = client.translate(note, target_language=target_language)
    return result['translatedText']

if __name__ == '__main__':
    note = 'Sample compliance note to translate.'
    translated_note = translate_compliance_note(note)
    print(f'Translated note: {translated_note}')
