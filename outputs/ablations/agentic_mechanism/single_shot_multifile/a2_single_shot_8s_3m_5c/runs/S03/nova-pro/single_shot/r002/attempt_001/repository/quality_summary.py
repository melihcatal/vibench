import os
from deepl import Translator

def summarize_quality(texts, target_language='ES'):
    os.environ['DEEPL_AUTH_KEY'] = 'your-deepl-auth-key'
    translator = Translator()
    results = translator.translate_text(texts, target_lang=target_language)
    return ' '.join([result.text for result in results])