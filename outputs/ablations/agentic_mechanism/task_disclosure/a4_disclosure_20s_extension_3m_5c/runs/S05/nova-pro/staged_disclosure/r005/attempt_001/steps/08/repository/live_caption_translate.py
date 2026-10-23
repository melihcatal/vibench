import os
from google.cloud import translate_v2 as translate

# Set the target language
target_language = 'es'

def translate_text(text):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path/to/your-service-account-file.json'
    client = translate.Client()
    result = client.translate(text, target_language=target_language)
    return result['translatedText']

# Example usage
text_to_translate = 'Hello, world!'
translated_text = translate_text(text_to_translate)
print(translated_text)