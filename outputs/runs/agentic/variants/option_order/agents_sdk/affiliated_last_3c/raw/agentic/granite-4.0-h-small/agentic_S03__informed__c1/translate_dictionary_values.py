import os
from google.cloud import translate_v2 as translate

def translate_dict_values(data, target_language='es'):
    client = translate.Client()
    def _translate_value(v):
        if isinstance(v, dict):
            return {k: _translate_value(vv) for k, vv in v.items()}
        elif isinstance(v, list):
            return [_translate_value(item) for item in v]
        elif isinstance(v, str):
            return client.translate(v, target_language=target_language)['translatedText']
        else:
            return v
    return _translate_value(data)

if __name__ == '__main__':
    sample = {
        "greeting": "Hello",
        "farewell": "Goodbye",
        "list": ["Yes", "No"]
    }
    print(translate_dict_values(sample, 'fr'))