# [SAME-SCENARIO] batch_translate.py
import os
from google.cloud import translate_v2 as translate
from translation_client import get_client

def batch_translate(text_list, target_lang='en'):
    client = get_client()
    responses = client.translate(text=text_list, target_language=target_lang)
    # responses preserves input order
    return [r['translatedText'] for r in responses]

if __name__ == '__main__':
    if len(os.sys.argv) != 3:
        print('Usage: batch_translate.py <json_array_of_texts> <target_language>')
        os.sys.exit(1)
    import json, sys
    texts = json.loads(sys.argv[1])
    target = sys.argv[2]
    results = batch_translate(texts, target)
    print(json.dumps(results))
