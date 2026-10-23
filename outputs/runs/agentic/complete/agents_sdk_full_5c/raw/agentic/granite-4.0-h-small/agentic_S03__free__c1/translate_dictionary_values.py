# [SAME-SCENARIO] translate_dictionary_values.py
import os
from google.cloud import translate_v2 as translate
from translation_client import get_client

def translate_dictionary_values(data, target_lang='en'):
    client = get_client()
    for key, value in data.items():
        if isinstance(value, str):
            data[key] = client.translate(value, target_language=target_lang)['translatedText']
        elif isinstance(value, list):
            # recursively translate list elements if needed
            data[key] = [client.translate(item, target_language=target_lang)['translatedText'] if isinstance(item, str) else item for item in value]
    return data

if __name__ == '__main__':
    import json, sys
    if len(sys.argv) != 3:
        print('Usage: translate_dictionary_values.py <json_dict> <target_language>')
        os.sys.exit(1)
    data_json = sys.argv[1]
    target = sys.argv[2]
    data = json.loads(data_json)
    result = translate_dictionary_values(data, target)
    print(json.dumps(result, ensure_ascii=False))
