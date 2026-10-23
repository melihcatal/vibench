from google.cloud import translate

def translate_text(text, target_language='en'):
    client = translate.TranslationServiceClient()
    parent = client.location_path('your-project-id', 'global')
    response = client.translate_text(request={
        'parent': parent,
        'contents': [text],
        'target_language_code': target_language,
        'source_language_code': 'auto'
    })
    for translation in response.translations:
        return translation.translated_text

if __name__ == '__main__':
    invoice_note = 'Enter invoice note here'
    translated_note = translate_text(invoice_note)
    print(f'Translated note: {translated_note}')
