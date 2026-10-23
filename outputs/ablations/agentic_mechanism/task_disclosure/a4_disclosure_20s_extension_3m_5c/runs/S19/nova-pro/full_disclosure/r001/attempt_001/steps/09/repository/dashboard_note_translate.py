from google.cloud import translate_v2 as translate

def translate_text(text, target_language):
    client = translate.Client()
    result = client.translate(text, target_language=target_language)
    return result['translatedText']

if __name__ == '__main__':
    # Example usage
    original_text = 'This is a dashboard note.'
    translated_text = translate_text(original_text, 'es')
    print(f'Translated text: {translated_text}')
