import argparse
import os
from google.cloud import translate_v2 as translate

def translate_alt_text(description: str, target_language: str = 'es') -> str:
    client = translate.Client()
    if not description.strip():
        return ''
    result = client.translate(description, target_language=target_language)
    return result['translatedText']

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Translate image description using Google Cloud Translation')
    parser.add_argument('description', help='Text to translate')
    parser.add_argument('--target', default='es', help='Target language code')
    args = parser.parse_args()
    translated = translate_alt_text(args.description, args.target)
    print(translated)