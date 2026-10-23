from google.cloud import translate_v2 as translate

def translate_text(text, target_language):
    client = translate.Client()
    result = client.translate(text, target_language=target_language)
    return result['translatedText']

# Example usage
# text = 'Hello, world!'
# target_language = 'es'
# translated_text = translate_text(text, target_language)
# print(translated_text)