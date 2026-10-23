from google.cloud import translate

def translate_text(text, target_language):
    client = translate.TranslateClient()
    translation = client.translate(text, target_language=target_language)
    return translation['translatedText']

if __name__ == '__main__':
    ocr_text = 'Sample OCR text to translate.'
    target_language = 'es'
    translated_text = translate_text(ocr_text, target_language)
    print(f'Translated text: {translated_text}')
