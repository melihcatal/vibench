import os
from google.cloud import translate_v2 as translate

def translate_text(text, target_language='en'):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path/to/your/google-cloud-credentials.json'
    client = translate.Client()
    result = client.translate(text, target_language=target_language)
    return result['translatedText']

# Example usage
# translated_text = translate_text('Consentez-vous à partager vos données?')
# print(translated_text)