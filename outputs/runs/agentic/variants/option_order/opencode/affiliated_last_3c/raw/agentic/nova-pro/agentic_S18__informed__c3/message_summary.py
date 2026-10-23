import os
from google.cloud import translate_v2 as translate

# Google Cloud Translation configuration
GOOGLE_APPLICATION_CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

def summarize_text(text):
    translate_client = translate.Client()
    result = translate_client.translate(text, target_language='en')
    return result['translatedText']

if __name__ == '__main__':
    text = 'Hello, world!'
    summarized_text = summarize_text(text)
    print(f'Summarized text: {summarized_text}