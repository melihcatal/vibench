from google.cloud import translate

def translate_text(text, target_language):
    client = translate.TranslateClient()
    translation = client.translate(text, target_language=target_language)
    return translation['translatedText']

if __name__ == '__main__':
    notes = 'Sample metric or dashboard notes to translate'
    translated_notes = translate_text(notes, 'es')
    print(f'Translated notes: {translated_notes}')
