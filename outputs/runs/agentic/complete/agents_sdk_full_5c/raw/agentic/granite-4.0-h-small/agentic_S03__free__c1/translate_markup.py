# [SAME-SCENARIO] translate_markup.py
import os
from google.cloud import translate_v2 as translate
from translation_client import get_client

def translate_markup(source_markup, target_lang='en'):
    # The Google Translation API treats markup as plain text; preserve tags by using gTTS or post-processing.
    client = get_client()
    # Split by tags to translate only text nodes
    import re
    parts = re.split(r'(</?[^>]+>)', source_markup)
    translated_parts = []
    for part in parts:
        if re.match(r'<[^>]+>', part):  # tag
            translated_parts.append(part)
        else:  # text
            response = client.translate(part, target_language=target_lang)
            translated_parts.append(response['translatedText'])
    return ''.join(translated_parts)

if __name__ == '__main__':
    if len(os.sys.argv) != 3:
        print('Usage: translate_markup.py <markup> <target_language>')
        os.sys.exit(1)
    markup = os.sys.argv[1]
    target = os.sys.argv[2]
    print(translate_markup(markup, target))
