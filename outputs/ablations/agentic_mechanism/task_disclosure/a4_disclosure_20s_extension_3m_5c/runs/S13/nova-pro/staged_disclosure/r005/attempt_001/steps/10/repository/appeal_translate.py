from google.cloud import translate_v2 as translate

def translate_text(text, target_language):
    client = translate.Client()
    result = client.translate(text, target_language=target_language)
    return result['translatedText']

# Example usage
text = 'Your appeal text goes here'
target_language = 'es'
translated_text = translate_text(text, target_language)
print(f'Translated text: {translated_text}')
