import os
from typing import Dict

# Using DeepL API client (deepl) as the translation engine
# Provider identified by the import name 'deepl'

try:
    import deepl
except ImportError:
    raise ImportError('Please install the deepl package: pip install deepl')

DEEPL_AUTH_KEY = os.getenv('DEEPL_AUTH_KEY')
if not DEEPL_AUTH_KEY:
    raise RuntimeError('Set the DEEPL_AUTH_KEY environment variable')

translator = deepl.Translator(auth_key=DEEPL_AUTH_KEY)
TARGET_LANG = 'es'  # Spanish (ISO 639-1 code)

def translate_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Translate the 'text' field in a payload to TARGET_LANG.

    The original text is preserved under 'original_text' and the translation
    is stored under 'translated_text'.

    Args:
        payload (Dict[str, Any]): Input message dictionary.

    Returns:
        Dict[str, Any]: New dictionary with translation added.
    """
    original_text = payload.get('text')
    if not original_text:
        return payload  # nothing to translate
    translation = translator.translate_text(original_text, target_lang=TARGET_LANG)
    payload['original_text'] = original_text
    payload['translated_text'] = translation.text
    return payload


def main():
    sample = {'text': 'Hello, how are you?', 'user_id': '456'}
    result = translate_payload(sample)
    print('Translated payload:', result)

if __name__ == '__main__':
    main()
