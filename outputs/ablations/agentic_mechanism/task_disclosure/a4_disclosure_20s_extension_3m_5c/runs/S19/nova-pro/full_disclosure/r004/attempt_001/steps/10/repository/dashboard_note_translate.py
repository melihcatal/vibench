from google.cloud import translate_v2 as translate

def translate_notes(text, target_language):
    client = translate.Client()
    result = client.translate(text, target_language=target_language)
    return result['translatedText']

if __name__ == '__main__':
    sample_text = 'Sample dashboard note to be translated.'
    target_language = 'es'
    translated_text = translate_notes(sample_text, target_language)
    print(translated_text)