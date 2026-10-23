import os
import json
from google.cloud import translate_v2 as translate

# Google Cloud Translation setup
GOOGLE_APPLICATION_CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
translator = translate.Client()

def translate_text(source_text: str, target_lang: str = 'en') -> str:
    """
    Translates arbitrary text to the target language using Google Cloud Translation.
    """
    if not source_text:
        return ""
    try:
        result = translator.translate(source_text, target_language=target_lang)
        return result['translatedText']
    except Exception as exc:
        print(f"Translation error: {exc}")
        return source_text  # fallback: return original

if __name__ == '__main__':
    sample = {'text': 'Bonjour tout le monde'}
    print('Translation:', translate_text(sample['text'], target_lang='en'))
