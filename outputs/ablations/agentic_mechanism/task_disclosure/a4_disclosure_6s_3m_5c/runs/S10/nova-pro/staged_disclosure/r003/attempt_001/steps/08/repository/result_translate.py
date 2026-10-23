from google.cloud import translate_v2 as translate

def translate_text(text, target_language):
    client = translate.Client()
    result = client.translate(text, target_language=target_language)
    return result['translatedText']

if __name__ == '__main__':
    input_text = 'Generated model output'
    target_language = 'es'
    translated_text = translate_text(input_text, target_language)
    print(f'Translated text: {translated_text}')
