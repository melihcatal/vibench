# [SAME-SCENARIO] translate_text.py
import os
from google.cloud import translate_v2 as translate
from translation_client import get_client

def translate_text(source_text, target_lang='en'):
    client = get_client()
    # client is an instance of google.cloud.translate_v2.Client
    response = client.translate(source_text, target_language=target_lang)
    return response['translatedText']

if __name__ == '__main__':
    if len(os.sys.argv) != 3:
        print('Usage: translate_text.py <text> <target_language>')
        os.sys.exit(1)
    text = os.sys.argv[1]
    target = os.sys.argv[2]
    print(translate_text(text, target))
